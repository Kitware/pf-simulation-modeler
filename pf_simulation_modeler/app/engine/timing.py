class TimingLogic:
    def __init__(self, state, ctrl):
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

        state.update(
            {
                "cycle_ids": [],
                "sub_cycle_ids": {},
                "timing_id": self.pxm.create("Timing").id,
            }
        )

        cycle = self.create_cycle("Cycle", Name="constant", Repeat=-1)
        self.create_cycle("SubCycle", cycle.id, Name="alltime", Length=1)

        cycle = self.create_cycle("Cycle", Name="rainrec", Repeat=-1)
        self.create_cycle("SubCycle", cycle.id, Name="rain")
        self.create_cycle("SubCycle", cycle.id, Name="rec")

        ctrl.delete_cycle = self.delete_cycle
        ctrl.create_cycle = self.create_cycle
        ctrl.update_cycle_list = self.update_cycle_list

    def delete_cycle(self, id, owner_id=None):
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
        cycle_ids = []
        sub_cycle_ids = {}
        for cycle in self.pxm.get_instances_of_type("Cycle"):
            cycle_ids.append(cycle.id)
            sub_cycle_ids[cycle.id] = []
            for sub_cycle_id in cycle.own:
                sub_cycle_ids[cycle.id].append(sub_cycle_id)

        self.state.cycle_ids = cycle_ids
        self.state.sub_cycle_ids = sub_cycle_ids


def initialize(server):
    state, ctrl = server.state, server.controller

    TimingLogic(state, ctrl)
