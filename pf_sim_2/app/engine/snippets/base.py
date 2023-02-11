from .timing import TimingSnippet
from .domain import DomainSnippet
from .domain_builder import DomainBuilderSnippet
from .boundary_conditions import BoundaryConditionsSnippet
from .subsurface_properties import SubsurfacePropertiesSnippet
from .solver import SolverSnippet


class PreambleSnippet:
    @property
    def snippet(self):
        return """# Parflow Simulation Modeler - Project Generation Code
from parflow import Run
from parflow.tools.builders import SubsurfacePropertiesBuilder, DomainBuilder


LW_Test = Run("LW_Test", __file__)

LW_Test.FileVersion = 4

LW_Test.Process.Topology.P = 1
LW_Test.Process.Topology.Q = 1
LW_Test.Process.Topology.R = 1
"""


def initialize(server):
    state, ctrl = server.state, server.controller

    timing_snippet = TimingSnippet(state, ctrl)
    domain_snippet = DomainSnippet(state, ctrl)
    domain_builder = DomainBuilderSnippet()
    boundary_snippet = BoundaryConditionsSnippet(state, ctrl)
    subsurface_snippet = SubsurfacePropertiesSnippet(state, ctrl)
    solver_snippet = SolverSnippet(state, ctrl)

    state.update(
        {
            "generated_code": "",
            "display_snippet": False,
            "active_snippet": "",
        }
    )

    @state.change("currentView")
    def clear_snippet(**kwargs):
        state.display_snippet = False

    @state.change("currentView")
    def generate_code(**kwargs):
        # Domain page
        domain_snippet.set_indicator_file()
        domain_snippet.set_grid()
        domain_snippet.set_soils()
        domain_snippet.set_terrain_files()

        # Timing page
        timing_snippet.set_timing_info()
        timing_snippet.set_cycles()

        # Boundary Conditions page
        boundary_snippet.set_boundary_conditions()

        # Subsurface Properties page
        subsurface_snippet.set_soils()

        # Solver page
        solver_snippet.set_output()
        solver_snippet.set_general()
        solver_snippet.set_nonlinear()
        solver_snippet.set_linear()

        # DomainBuilder params
        domain_builder_params = {
            **boundary_snippet.domain_builder_params,
            **domain_snippet.domain_builder_params,
            **state.simTypeShortcuts,
        }

        code = "\n".join(
            [
                PreambleSnippet().snippet,
                domain_snippet.snippet,
                timing_snippet.snippet,
                domain_builder.snippet(domain_builder_params),
                boundary_snippet.snippet,
                subsurface_snippet.snippet,
                solver_snippet.snippet,
                "\nLW_Test.run()\n",
            ]
        )
        state.generated_code = code
        return code

    def get_snippet(snippet):
        generate_code()
        if snippet == "domain":
            state.active_snippet = domain_snippet.snippet
        elif snippet == "timing":
            state.active_snippet = timing_snippet.snippet
        elif snippet == "boundary_conditions":
            state.active_snippet = boundary_snippet.snippet
        elif snippet == "subsurface_properties":
            state.active_snippet = subsurface_snippet.snippet
        elif snippet == "solver":
            state.active_snippet = solver_snippet.snippet
        else:
            state.active_snippet = "# Error: No snippet found"

    def toggle_snippet(snippet):
        state.display_snippet = not state.display_snippet
        if state.display_snippet:
            get_snippet(snippet)

    ctrl.toggle_snippet = toggle_snippet
    ctrl.generate_code = generate_code
    ctrl.get_snippet = get_snippet
