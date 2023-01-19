from .timing import TimingSnippet
from .domain import DomainSnippet
from .domain_builder import DomainBuilderSnippet


class PreambleSnippet:
    @property
    def snippet(self):
        return """# Parflow Simulation Modeler - Project Generation Snippets
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

    def generate_snippets():
        # Timing page
        timing_snippet.set_timing_info(state.timingId)

        # Domain page
        domain_snippet.set_indicator_file(state.indicatorFileName)
        domain_snippet.set_grid(state.gridId)
        domain_snippet.set_soils(state.soilIds)
        domain_snippet.set_terrain_files(state.slopeXFile, state.slopeYFile)

        domain_builder_params = {
            **domain_snippet.domain_builder_params,
            **state.simTypeShortcuts,
        }

        print(domain_builder_params)

        return "\n\n".join(
            [
                PreambleSnippet().snippet,
                domain_builder.snippet(domain_builder_params),
                timing_snippet.snippet,
                domain_snippet.snippet,
            ]
        )

    ctrl.generate_snippets = generate_snippets

    @state.change("currentView")
    def on_currentView_change(currentView, **kwargs):
        code = generate_snippets()
        print(f'Code:\n{code}')
