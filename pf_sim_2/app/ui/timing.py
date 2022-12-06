from trame.widgets import vuetify, html, simput


class Timing:
    def __init__(self, server):
        state, ctrl = server.state, server.controller
        self.server = server
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

        state.update(
            {
                "cycleIds": [],
                "subCycleIds": {},
            }
        )

        cycle = self.create_cycle("Cycle", Name="constant", repeat=-1)
        self.create_cycle("SubCycle", cycle.id, Name="alltime", Length=1)

        cycle = self.create_cycle("Cycle", Name="rainrec", repeat=-1)
        self.create_cycle("SubCycle", cycle.id, Name="rain")
        self.create_cycle("SubCycle", cycle.id, Name="rec")

    def delete_cycle(self, id, proxy_type, owner_id=None):
        if owner_id is not None:
            owner = self.pxm.get(owner_id)
            owner._own.remove(id)

        self.pxm.delete(id)

        self.update_cycle_list()

    def create_cycle(self, proxy_type, owner_id=None, **kwargs):
        proxy = self.pxm.create(proxy_type, **kwargs)

        if owner_id is not None:
            owner = self.pxm.get(owner_id)
            owner._own.add(proxy.id)

        self.update_cycle_list()

        return proxy

    def update_cycle_list(self, *args, **kwargs):
        cycleIds = []
        subCycleIds = {}
        for cycle in self.pxm.get_instances_of_type("Cycle"):
            cycleIds.append(cycle.id)
            subCycleIds[cycle.id] = []
            for subCycleId in cycle.own:
                subCycleIds[cycle.id].append(subCycleId)

        self.state.cycleIds = cycleIds
        self.state.subCycleIds = subCycleIds

    def page(self):
        html.H1("Timing")
        simput.SimputItem(item_id=("timingId",))

        html.H1("Cycles")

        with vuetify.VContainer(v_for=("(cycleId, index) in cycleIds",), fluid=True):
            with vuetify.VContainer(style="display: flex;", fluid=True):
                simput.SimputItem(item_id=("cycleId",), style="flex-grow: 1;")
                with vuetify.VBtn(
                    click=(self.delete_cycle, "[cycleId, 'Cycle']"),
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
                        click=(self.delete_cycle, "[subId, 'SubCycle', cycleId]"),
                        small=True,
                        icon=True,
                    ):
                        vuetify.VIcon("mdi-delete")

                with vuetify.VBtn(click=(self.create_cycle, "['SubCycle', cycleId]")):
                    vuetify.VIcon("mdi-plus")
                    html.Span("Add Sub Cycle")

        with vuetify.VBtn(click=(self.create_cycle, "['Cycle']")):
            vuetify.VIcon("mdi-plus")
            html.Span("Add Cycle")
