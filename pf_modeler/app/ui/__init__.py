from pf_modeler.app.engine.simput import KeyDatabase
from trame import state, controller as ctrl
from trame.layouts import SinglePage
from trame.html import vuetify, simput, Div, Element
from pf_modeler import html as pf_widgets
from .domain import create_ui as create_domain_ui, initialize as initialize_domain_ui
from .output import create_project_generation
from .timing import create_ui as create_timing_ui, initialize as initialize_timing_ui
from .boundary_conditions import create_ui as create_bc_ui, initialize as initialize_bc_ui

# -----------------------------------------------------------------------------
# Initialization helper
# -----------------------------------------------------------------------------
def initialize():
    initialize_domain_ui()
    initialize_timing_ui()
    initialize_bc_ui()

def initialize_simput():
    key_database = KeyDatabase()
    layout.root = simput.Simput(
        key_database.ui_manager,
        key_database.pdm,
        prefix="simput",
    )


ctrl.ui_set_key_database = initialize_simput

# -----------------------------------------------------------------------------
# Main layout
# -----------------------------------------------------------------------------
layout = SinglePage("Parflow Simulation Modeler")
layout.title.set_text("Parflow Simulation Modeler")
layout.logo.children = [vuetify.VIcon("mdi-water-opacity", color="blue", large=True)]

# -----------------------------------------------------------------------------
# Toolbar
# -----------------------------------------------------------------------------
with layout.toolbar as tb:
    vuetify.VSpacer()
    pf_widgets.NavigationDropDown(v_model="currentView", views=("views",))
    vuetify.VSpacer()
    vuetify.VBtn("Save", click=ctrl.simput_save)
    layout.content.style = "padding-left: 2rem; padding-right: 2rem;"


# -----------------------------------------------------------------------------
# Main content
# -----------------------------------------------------------------------------
with layout.content as content:
    pf_widgets.FileDatabase(
        files=("dbFiles",),
        fileCategories=("fileCategories",),
        error=("uploadError",),
        db_update="updateFiles",
        v_model="dbSelectedFile",
        v_if="currentView == 'File Database'",
    )
    pf_widgets.SimulationType(
        v_if="currentView == 'Simulation Type'",
        shortcuts=(
            "simTypeShortcuts",
            {
                "wells": False,
                "climate": True,
                "contaminants": False,
                "saturated": "Variably Saturated",
            },
        ),
    )

    create_domain_ui()

    with Div(v_if="currentView == 'Timing'"):
        create_timing_ui()

    with Div(v_if="currentView == 'Boundary Conditions'"):
        create_bc_ui()

    with Div(v_if="currentView == 'Subsurface Properties'") as d:
        Element("H1", "Regions")

        simput.SimputItem(
            v_for=("(soilId, index) in soilIds",),
            itemId=("soilId",),
        )

    create_project_generation(
        validation_callback=ctrl.validate_run,
        validation_output="projGenValidation.output",
        validation_check="projGenValidation.valid",
    )


# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
# layout.footer.hide()
