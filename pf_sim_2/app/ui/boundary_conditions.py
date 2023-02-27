from trame_server.utils.hot_reload import hot_reload
from trame.widgets import vuetify, html, simput
from .snippet import show_snippet


@hot_reload
def boundary_conditions(ctrl):
    html.H1("Boundary Conditions")

    with vuetify.VContainer(v_for=("(id, i) in bc_pressure_ids",), fluid=True):
        simput.SimputItem(item_id=("id",))
        with vuetify.VContainer(fluid=True, style="padding: 3rem;"):
            simput.SimputItem(
                v_for=("(value_id, vi) in bc_pressure_value_ids[id]",),
                item_id=("value_id",),
            )

    show_snippet(ctrl, "boundary_conditions")
