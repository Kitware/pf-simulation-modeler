from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, simput, html, code
from pf_sim_2.widgets import pf_sim_2 as pf_widgets
from .domain import domain
from .timing import timing
from .solver import solver
from .boundary_conditions import boundary_conditions
from .snippet import show_snippet


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

            self.simput_widget.clear()
            layout.root = self.simput_widget

            with layout.toolbar:
                vuetify.VSpacer()
                pf_widgets.NavigationDropDown(v_model="current_view", views=("views",))
                vuetify.VSpacer()
                vuetify.VBtn("Save", click=self.ctrl.simput_apply)

            # Main content
            with layout.content:
                with vuetify.VContainer(fluid=True):
                    pf_widgets.FileDatabase(
                        v_if="current_view === 'File Database'",
                        files=("db_files",),
                        fileCategories=("file_categories",),
                        error=("upload_error",),
                        v_model=("db_selected_file",),
                    )

                    pf_widgets.SimulationType(
                        v_if="current_view === 'Simulation Type'",
                        v_model=(
                            "simTypeShortcuts",
                            {
                                "wells": False,
                                "climate": True,
                                "contaminants": False,
                                "saturated": "Variably Saturated",
                            },
                        ),
                    )

                    with html.Div(v_if="current_view === 'Domain'"):
                        domain(self.ctrl)

                    with html.Div(v_if="current_view === 'Timing'"):
                        timing(self.ctrl)

                    with html.Div(v_if="current_view === 'Boundary Conditions'"):
                        boundary_conditions(self.ctrl)

                    with html.Div(v_if="current_view === 'Subsurface Properties'"):
                        html.H1("Regions")

                        with html.Div(v_if="soil_ids.length === 0"):
                            html.H2("No regions defined")
                            html.P("Choose an indicator file to define regions.")

                        with html.Div(v_if="soil_ids.length > 0"):
                            simput.SimputItem(item_id=("domain_id", None))
                            simput.SimputItem(
                                v_for=("(soil_id, index) in soil_ids",),
                                item_id=("soil_id", None),
                            )
                        show_snippet(self.ctrl, "subsurface_properties")

                    with html.Div(v_if="current_view === 'Solver'"):
                        solver(self.ctrl)

                    with html.Div(v_if="current_view === 'Code Generation'"):
                        html.H1("Generator")
                        with vuetify.VContainer(
                            fluid=True, classes="fill-height pa-0 justify-center"
                        ):
                            code.Editor(
                                style="width: 100%; height: 85vh;",
                                value=("generated_code",),
                                options=("editor_options", {}),
                                language="python",
                                theme=("editor_theme", "vs-dark"),
                            )
