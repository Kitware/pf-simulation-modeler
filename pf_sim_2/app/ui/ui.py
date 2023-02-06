from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, simput, html
from pf_sim_2.widgets import pf_sim_2 as pf_widgets
from .domain import domain
from .timing import timing
from .solver import solver
from .boundary_conditions import boundary_conditions


def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "Parflow Simulation Modeler"

    simput_widget = simput.Simput(ctrl.get_simput_manager(), trame_server=server)
    ctrl.simput_apply = simput_widget.apply
    ctrl.simput_reset = simput_widget.reset
    simput_widget.reload_domain()

    with SinglePageLayout(server) as layout:
        # Toolbar
        layout.title.set_text("Parflow Simulation Modeler")
        layout.icon.add_child(
            vuetify.VIcon("mdi-water-opacity", color="blue", large=True)
        )
        layout.root = simput_widget

        with layout.toolbar:
            vuetify.VSpacer()
            pf_widgets.NavigationDropDown(v_model="currentView", views=("views",))
            vuetify.VSpacer()
            vuetify.VBtn("Save", click=ctrl.simput_apply)

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True):
                pf_widgets.FileDatabase(
                    v_if="currentView === 'File Database'",
                    files=("dbFiles",),
                    fileCategories=("fileCategories",),
                    error=("uploadError",),
                    v_model=("dbSelectedFile",),
                )
                pf_widgets.SimulationType(
                    v_if="currentView === 'Simulation Type'",
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

                with html.Div(v_if="currentView === 'Domain'"):
                    domain()

                with html.Div(v_if="currentView === 'Timing'"):
                    timing(ctrl)

                with html.Div(v_if="currentView === 'Boundary Conditions'"):
                    boundary_conditions()

                with html.Div(v_if="currentView === 'Subsurface Properties'"):
                    html.H1("Regions")

                    with html.Div(v_if="soilIds.length === 0"):
                        html.H2("No regions defined")
                        html.P("Choose an indicator file to define regions.")

                    with html.Div(v_if="soilIds.length > 0"):
                        simput.SimputItem(item_id=("domainId", None))
                        simput.SimputItem(
                            v_for=("(soilId, index) in soilIds",),
                            item_id=("soilId", None),
                        )

                with html.Div(v_if="currentView === 'Solver'"):
                    solver()

                with html.Div(v_if="currentView === 'Code Generation'"):
                    html.H1("Generator")

                    vuetify.VTextarea(
                        v_model=("generated_code",), rows=28, row_height=20
                    )
