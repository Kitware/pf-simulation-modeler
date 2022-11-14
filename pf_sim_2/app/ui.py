from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, simput
from pf_sim_2.widgets import pf_sim_2 as pf_widgets
from pathlib import Path
from .domain import Domain

from trame_simput import get_simput_manager

DEF_DIR = Path('/home/local/KHQ/will.dunklin/Desktop/work/pf_sim_2/pf_sim_2/app/definitions')

def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "pf_sim_2"

    # Initialize UI components

    simput_manager = get_simput_manager()
    simput_manager.load_model(yaml_file=DEF_DIR / "grid.yaml")
    simput_manager.load_ui(xml_file=DEF_DIR / "grid_ui.xml")

    domain = Domain(server, simput_manager.proxymanager)

    simput_widget = simput.Simput(simput_manager, trame_server=server)
    ctrl.simput_apply = simput_widget.apply
    ctrl.simput_reset = simput_widget.reset

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
                    db_update="updateFiles",
                    v_model="dbSelectedFile",
                    uploadFile=(ctrl.uploadFile, "[$event]"),
                    uploadLocalFile=ctrl.uploadLocalFile,
                    updateFiles=ctrl.updateFiles,
                )
                pf_widgets.SimulationType(
                    v_if="currentView === 'Simulation Type'",
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

            domain.page()
            #     simput.SimputItem(item_id=('active_id', None))
