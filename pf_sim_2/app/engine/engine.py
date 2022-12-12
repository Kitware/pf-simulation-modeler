r"""
Define your classes and create the instances that you need to expose
"""
import logging
from pathlib import Path
import yaml
from trame_simput import get_simput_manager
from . import files
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
                    "Project Generation",
                ],
            }
        )

        # Simput
        self.simput_manager = get_simput_manager()

        self.pxm = self.simput_manager.proxymanager

        ctrl.get_pxm = lambda: self.pxm
        ctrl.get_simput_manager = lambda: self.simput_manager

        # add item
        self.simput_manager.load_model(yaml_file=DEF_DIR / "grid.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "grid_ui.xml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "cycle.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "cycle_ui.xml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "timing.yaml")
        self.simput_manager.load_model(yaml_file=DEF_DIR / "boundary.yaml")
        self.simput_manager.load_ui(xml_file=DEF_DIR / "boundary_ui.xml")

        state.gridId = self.pxm.create("ComputationalGrid").id
        state.timingId = self.pxm.create("Timing").id

        # on view change
        state.change("currentView", self.on_currentView_change)

    def on_currentView_change(self, currentView, **kwargs):
        if currentView == "Boundary Conditions":
            model_file = DEF_DIR / "boundary.yaml"
            with open(model_file) as f:
                model = yaml.load(f)

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

            model_content = yaml.dump(model)
            self.simput_manager.load_model(yaml_content=model_content)
            self.simput_manager.load_language(yaml_content=model_content)


# ---------------------------------------------------------
# Server binding
# ---------------------------------------------------------


def initialize(server):
    state, ctrl = server.state, server.controller

    args = server.cli.parse_known_args()[0]
    print(args)

    validator = ArgumentsValidator(args)
    if not validator.valid:
        raise RuntimeError("Invalid arguments")

    files.initialize(server, validator.args)

    # @state.change("resolution")
    # def resolution_changed(resolution, **kwargs):
    #     logger.info(f">>> ENGINE(b): Slider updating resolution to {resolution}")

    engine = MyBusinessLogic(server)
    return engine
