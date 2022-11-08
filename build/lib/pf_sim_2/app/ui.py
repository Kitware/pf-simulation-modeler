from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, simput
from pf_sim_2.widgets import pf_sim_2 as my_widgets
from pathlib import Path

from trame_simput import get_simput_manager

DEF_DIR = Path('/home/local/KHQ/will.dunklin/Desktop/work/pf_sim_2/pf_sim_2/app/definitions')

def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "pf_sim_2"

    simput_manager = get_simput_manager()
    simput_manager.load_model(yaml_file=DEF_DIR / "model.yaml")
    simput_manager.load_ui(xml_file=DEF_DIR / "ui.xml")

    simput_widget = simput.Simput(simput_manager, prefix="ab", trame_server=server)
    ctrl.simput_apply = simput_widget.apply
    ctrl.simput_reset = simput_widget.reset

    def create():
        person = simput_manager.proxymanager.create('Person')
        state.active_id = person.id

    with SinglePageLayout(server) as layout:
        # Toolbar
        layout.title.set_text("Test")
        layout.root = simput_widget

        with layout.toolbar:
            vuetify.VSpacer()
            with vuetify.VBtn(icon=True, click=create):
                vuetify.VIcon("mdi-plus")

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True):
                simput.SimputItem(item_id=('active_id', None))
