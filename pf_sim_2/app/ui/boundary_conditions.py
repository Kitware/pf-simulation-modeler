from trame_server.utils.hot_reload import hot_reload
from trame.widgets import vuetify, html, simput
from .snippet import show_snippet


@hot_reload
def boundary_conditions(ctrl):
    with vuetify.VContainer(classes="pa-2 pt-4"):
        html.H1("Boundary Conditions")

        with vuetify.VContainer(v_for=("(id, i) in bc_pressure_ids",), fluid=True):
            simput.SimputItem(item_id=("id",))
            with vuetify.VContainer(classes="pa-4 mb-0", fluid=True):
                simput.SimputItem(
                    v_for=("(value_id, vi) in bc_pressure_value_ids[id]",),
                    item_id=("value_id",),
                )

        show_snippet(ctrl, "boundary_conditions")
