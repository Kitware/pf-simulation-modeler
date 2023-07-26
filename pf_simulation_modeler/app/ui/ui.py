from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, simput, html
from pf_simulation_modeler.widgets import pfsm as pf_widgets
from .save_project import save_project_button
from .file_db import file_db
from .simulation_type import simulation_type
from .domain import domain
from .timing import timing
from .boundary_conditions import boundary_conditions
from .pressure import pressure
from .subsurface_props import subsurface_props
from .solver import solver
from .code_gen import code_gen


class UI:
    def __init__(self, server):
        self.server = server

        self.state, self.ctrl = server.state, server.controller
        self.state.trame__title = "Parflow Simulation Modeler"

        self.simput_widget = simput.Simput(
            self.ctrl.get_simput_manager(), trame_server=server
        )
        self.ctrl.simput_apply = self.simput_widget.apply
        self.ctrl.simput_reset = self.simput_widget.reset
        self.ctrl.simput_push = self.simput_widget.push
        self.simput_widget.reload_domain()

        self.ctrl.add("on_server_reload")(self.update_ui)
        self.update_ui()

    def update_ui(self, *args, **kwargs):
        with SinglePageLayout(self.server) as layout:
            layout.title.set_text("Parflow Simulation Modeler")
            with layout.icon:
                vuetify.VIcon("mdi-water-opacity", color="blue", large=True)

            self.simput_widget.register_layout(layout)

            with layout.toolbar:
                vuetify.VSpacer()
                pf_widgets.NavigationDropDown(v_model="current_view", views=("views",))
                vuetify.VSpacer()
                save_project_button(self.ctrl, self.state)

            # Main content
            with layout.content:
                with vuetify.VContainer(fluid=True, classes="pa-0"):
                    with html.Div(v_if="current_view === 'File Database'"):
                        file_db()

                    with html.Div(v_if="current_view === 'Simulation Type'"):
                        simulation_type()

                    with html.Div(v_if="current_view === 'Domain'"):
                        domain(self.ctrl)

                    with html.Div(v_if="current_view === 'Timing'"):
                        timing(self.ctrl)

                    with html.Div(v_if="current_view === 'Boundary Conditions'"):
                        boundary_conditions(self.ctrl)

                    with html.Div(v_if="current_view === 'Pressure'"):
                        pressure(self.ctrl)

                    with html.Div(v_if="current_view === 'Subsurface Properties'"):
                        subsurface_props(self.ctrl)

                    with html.Div(v_if="current_view === 'Solver'"):
                        solver(self.ctrl)

                    with html.Div(v_if="current_view === 'Code Generation'"):
                        code_gen()
