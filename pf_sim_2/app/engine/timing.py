class TimingLogic:
    def __init__(self, state, ctrl):
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

        state.timingId = self.pxm.create("Timing").id
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

        ctrl.delete_cycle = self.delete_cycle
        ctrl.create_cycle = self.create_cycle
        ctrl.update_cycle_list = self.update_cycle_list

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


def initialize(server):
    state, ctrl = server.state, server.controller

    TimingLogic(state, ctrl)
