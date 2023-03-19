from .timing import TimingSnippet
from .domain import DomainSnippet
from .domain_builder import DomainBuilderSnippet
from .boundary_conditions import BoundaryConditionsSnippet
from .subsurface_properties import SubsurfacePropertiesSnippet
from .solver import SolverSnippet


class PreambleSnippet:
    def __init__(self, state):
        self.state = state

    @property
    def snippet(self):
        return f"""\
# Parflow Simulation Modeler - Project Generation Code
from parflow import Run
from parflow.tools.builders import SubsurfacePropertiesBuilder, DomainBuilder


{self.state.sim_name} = Run("{self.state.sim_name}", __file__)

{self.state.sim_name}.FileVersion = 4

{self.state.sim_name}.Process.Topology.P = 1
{self.state.sim_name}.Process.Topology.Q = 1
{self.state.sim_name}.Process.Topology.R = 1
"""


def initialize(server):
    state, ctrl = server.state, server.controller

    preamble = PreambleSnippet(state)
    timing_snippet = TimingSnippet(state, ctrl)
    domain_snippet = DomainSnippet(state, ctrl)
    domain_builder = DomainBuilderSnippet(state)
    boundary_snippet = BoundaryConditionsSnippet(state, ctrl)
    subsurface_snippet = SubsurfacePropertiesSnippet(state, ctrl)
    solver_snippet = SolverSnippet(state, ctrl)

    state.update(
        {
            "generated_code": "",
            "display_snippet": False,
            "active_snippet": "",
            "snippet_dirty": False,
        }
    )

    def set_snippet_dirty(topic, **kwargs):
        if topic == "changed":
            state.snippet_dirty = True

    pxm = ctrl.get_pxm()
    pxm.on(set_snippet_dirty)

    @state.change("current_view")
    def generate_code(**kwargs):
        state.snippet_dirty = False

        # Domain page
        domain_code = domain_snippet.snippet

        # Boundary Conditions page
        boundary_code = boundary_snippet.snippet

        # DomainBuilder params
        domain_builder_params = {
            **boundary_snippet.domain_builder_params,
            **domain_snippet.domain_builder_params,
            **state.simTypeShortcuts,
        }

        snippets = [
            preamble.snippet,
            domain_code,
            timing_snippet.snippet,
            domain_builder.snippet(domain_builder_params),
            boundary_code,
            subsurface_snippet.snippet,
            solver_snippet.snippet,
            f"\n{state.sim_name}.run()\n",
        ]

        code = "\n".join([s for s in snippets if s])
        state.generated_code = code
        return code

    def get_snippet(snippet):
        state.snippet_dirty = False

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
