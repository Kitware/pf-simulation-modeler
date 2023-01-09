from trame.widgets import vuetify, html, simput


def timing(ctrl):
    html.H1("Timing")
    simput.SimputItem(item_id=("timingId",))

    html.H1("Cycles")

    with vuetify.VContainer(v_for=("(cycleId, index) in cycleIds",), fluid=True):
        with vuetify.VContainer(style="display: flex;", fluid=True):
            simput.SimputItem(item_id=("cycleId",), style="flex-grow: 1;")
            with vuetify.VBtn(
                click=(ctrl.delete_cycle, "[cycleId, 'Cycle']"),
                small=True,
                icon=True,
            ):
                vuetify.VIcon("mdi-delete")

        with vuetify.VContainer(fluid=True, style="padding: 2rem;"):
            with vuetify.VContainer(
                v_for=("(subId, subI) in subCycleIds[cycleId]",),
                fluid=True,
                style="display: flex;",
            ):
                simput.SimputItem(item_id=("subId",), style="flex-grow: 1;")

                with vuetify.VBtn(
                    click=(ctrl.delete_cycle, "[subId, 'SubCycle', cycleId]"),
                    small=True,
                    icon=True,
                ):
                    vuetify.VIcon("mdi-delete")

            with vuetify.VBtn(click=(ctrl.create_cycle, "['SubCycle', cycleId]")):
                vuetify.VIcon("mdi-plus")
                html.Span("Add Sub Cycle")

    with vuetify.VBtn(click=(ctrl.create_cycle, "['Cycle']")):
        vuetify.VIcon("mdi-plus")
        html.Span("Add Cycle")
