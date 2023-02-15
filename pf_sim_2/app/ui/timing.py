from trame.widgets import vuetify, html, simput
from .snippet import show_snippet


def timing(ctrl):
    html.H1("Timing")
    simput.SimputItem(item_id=("timing_id",))

    html.H1("Cycles")

    with vuetify.VContainer(v_for=("(cycle_id, index) in cycle_ids",), fluid=True):
        with vuetify.VContainer(style="display: flex;", fluid=True):
            simput.SimputItem(item_id=("cycle_id",), style="flex-grow: 1;")
            with vuetify.VBtn(
                click=(ctrl.delete_cycle, "[cycle_id, 'Cycle']"),
                small=True,
                icon=True,
            ):
                vuetify.VIcon("mdi-delete")

        with vuetify.VContainer(fluid=True, style="padding: 2rem;"):
            with vuetify.VContainer(
                v_for=("(sub_id, sub_i) in sub_cycle_ids[cycle_id]",),
                fluid=True,
                style="display: flex;",
            ):
                simput.SimputItem(item_id=("sub_id",), style="flex-grow: 1;")

                with vuetify.VBtn(
                    click=(ctrl.delete_cycle, "[sub_id, 'SubCycle', cycle_id]"),
                    small=True,
                    icon=True,
                ):
                    vuetify.VIcon("mdi-delete")

            with vuetify.VBtn(click=(ctrl.create_cycle, "['SubCycle', cycle_id]")):
                vuetify.VIcon("mdi-plus")
                html.Span("Add Sub Cycle")

    with vuetify.VBtn(click=(ctrl.create_cycle, "['Cycle']")):
        vuetify.VIcon("mdi-plus")
        html.Span("Add Cycle")

    show_snippet(ctrl, "timing")
