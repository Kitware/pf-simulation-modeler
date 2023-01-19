from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, simput, html
from pf_sim_2.widgets import pf_sim_2 as pf_widgets
from .domain import domain
from .timing import timing
from .boundary_conditions import BoundaryConditions


def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "pf_sim_2"

    # Initialize UI components
    boundary_conditions = BoundaryConditions(server)

    simput_widget = simput.Simput(ctrl.get_simput_manager(), trame_server=server)
    ctrl.simput_apply = simput_widget.apply
    ctrl.simput_reset = simput_widget.reset
    simput_widget.reload_domain()

    with SinglePageLayout(server) as layout:
        # Toolbar
        layout.title.set_text("PF Migration Test")
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
                    boundary_conditions.page()

                with html.Div(v_if="currentView === 'Subsurface Properties'"):
                    html.H1("Regions")

                    simput.SimputItem(
                        v_for=("(soilId, index) in soilIds",), item_id=("soilId", None)
                    )
