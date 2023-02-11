from trame.widgets import vuetify, html, simput
from .snippet import show_snippet


def boundary_conditions(ctrl):
    html.H1("Boundary Conditions")

    with vuetify.VContainer(v_for=("(id, i) in BCPressureIds",), fluid=True):
        simput.SimputItem(item_id=("id",))
        with vuetify.VContainer(fluid=True, style="padding: 3rem;"):
            simput.SimputItem(
                v_for=("(valueId, vi) in BCPressureValueIds[id]",),
                item_id=("valueId",),
            )

    show_snippet(ctrl, "boundary_conditions")
