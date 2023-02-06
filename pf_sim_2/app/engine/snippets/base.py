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
import sys
from parflow import Run
from parflow.tools.fs import get_absolute_path
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

    state.generated_code = ""

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

        code = "\n\n".join(
            [
                PreambleSnippet().snippet,
                domain_builder.snippet(domain_builder_params),
                timing_snippet.snippet,
                domain_snippet.snippet,
                boundary_snippet.snippet,
                subsurface_snippet.snippet,
                solver_snippet.snippet,
            ]
        )
        state.generated_code = code
        return code

    ctrl.generate_code = generate_code
