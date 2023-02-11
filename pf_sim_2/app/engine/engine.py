r"""
Define your classes and create the instances that you need to expose
"""
import logging
from pathlib import Path
import yaml
from trame_simput import get_simput_manager
from . import files
from . import domain
from . import timing
from . import snippets
from . import boundary_conditions
from . import solver
from .cli import ArgumentsValidator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEF_DIR = Path(
    "/home/local/KHQ/will.dunklin/Desktop/work/pf_sim_2/pf_sim_2/app/engine/model"
)

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class MyBusinessLogic:
    def __init__(self, server):
        self._server = server

        state, ctrl = server.state, server.controller
        self.state = state

        state.update(
            {
                "currentView": "File Database",
                "views": [
                    "File Database",
                    "Simulation Type",
                    "Domain",
                    "Timing",
                    "Boundary Conditions",
                    "Subsurface Properties",
                    "Solver",
                    # "Project Generation",
                    "Code Generation",
                ],
                "cycle_defs": {},
                "subcycle_defs": {},
            }
        )

        # Simput
        self.simput_manager = get_simput_manager()
        self.pxm = self.simput_manager.proxymanager
        ctrl.get_pxm = lambda: self.pxm
        ctrl.get_simput_manager = lambda: self.simput_manager

        # Load models
        self.simput_manager.load_model(yaml_file=DEF_DIR / "grid.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "grid_ui.xml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "domain.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "domain_ui.xml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "cycle.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "cycle_ui.xml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "timing.yaml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "boundary.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "boundary_ui.xml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "soil.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "soil_ui.xml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "solver.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "solver_ui.xml")

        # on view change
        @state.change("currentView")
        def on_currentView_change(currentView, **kwargs):
            if currentView == "Boundary Conditions":
                model_file = DEF_DIR / "boundary.yaml"
                with open(model_file) as f:
                    model = yaml.safe_load(f)

                cycles = list(
                    map(
                        lambda cycle: {"text": cycle["Name"], "value": cycle.id},
                        self.pxm.get_instances_of_type("Cycle"),
                    )
                )

                model["BCPressure"]["Cycle"]["domains"] = [
                    {"type": "LabelList", "values": cycles}
                ]

                sub_cycles = list(
                    map(
                        lambda cycle: {"text": cycle["Name"], "value": cycle.id},
                        self.pxm.get_instances_of_type("SubCycle"),
                    )
                )

                model["BCPressureValue"]["SubCycle"]["domains"] = [
                    {"type": "LabelList", "values": sub_cycles}
                ]

                state.cycle_defs = {cycle["value"]: cycle["text"] for cycle in cycles}
                state.subcycle_defs = {
                    cycle["value"]: cycle["text"] for cycle in sub_cycles
                }

                model_content = yaml.dump(model)
                self.simput_manager.load_model(yaml_content=model_content)
                self.simput_manager.load_language(yaml_content=model_content)


# ---------------------------------------------------------
# Server binding
# ---------------------------------------------------------
def initialize(server):
    engine = MyBusinessLogic(server)

    args = server.cli.parse_known_args()[0]
    print(args)

    validator = ArgumentsValidator(args)
    if not validator.valid:
        raise RuntimeError("Invalid arguments")

    files.initialize(server, validator.args)
    domain.initialize(server)
    timing.initialize(server)
    boundary_conditions.initialize(server)
    solver.initialize(server)

    snippets.initialize(server)

    return engine
