from trame_simput.core.proxy import Proxy
from functools import partial


class BCLogic:
    def __init__(self, state, ctrl):
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

        patches = self.get_patch_names()
        bc_pressures = list(
            map(lambda patch: self.pxm.create("BCPressure", Patch=patch), patches)
        )
        for bcp in bc_pressures:
            bcp.on(partial(self.on_bcp_change, id=bcp.id))

        bc_pressure_ids = list(map(lambda bcp: bcp.id, bc_pressures))

        state.update(
            {
                "bc_pressure_ids": bc_pressure_ids,
                "bc_pressure_value_ids": {},
                "bc_patch_names": self.get_patch_names(),
            }
        )

        patches_proxy: Proxy = self.pxm.get(self.state.patches_id)
        if not patches_proxy:
            raise Exception(f"Patches proxy [{self.state.patches_id}] not found.")
        patches_proxy.on(self.on_patch_name_change)

    def get_patch_names(self):
        patch_names = ["XLower", "XUpper", "YLower", "YUpper", "ZLower", "ZUpper"]
        patches_proxy: Proxy = self.pxm.get(self.state.patches_id)
        if not patches_proxy:
            return []
        return [patches_proxy.get_property(name) for name in patch_names]

    def on_patch_name_change(self, topic, **kwargs):
        if topic != "update":
            return

        patches = self.get_patch_names()
        for i, bcp_id in enumerate(self.state.bc_pressure_ids):
            bcp: Proxy = self.pxm.get(bcp_id)
            if not bcp:
                continue

            bcp.set_property("Patch", patches[i])
            bcp.commit()
            self.ctrl.simput_push(id=bcp_id)
        self.state.bc_patch_names = patches

    def on_bcp_change(self, topic, id, **kwargs):
        if topic != "update" and kwargs.get("property_name") != "Cycle":
            return

        bcp = self.pxm.get(id)
        cycle_id = bcp["Cycle"]

        cycle = self.pxm.get(cycle_id)
        if not cycle:
            return

        # Delete values defined for other cycles
        for value_id in self.state.bc_pressure_value_ids.get(id, []):
            self.pxm.delete(value_id)

        # Create new values for the new cycle
        bc_pressure_value_ids = {**self.state.bc_pressure_value_ids}
        bc_pressure_value_ids[id] = [
            self.pxm.create("BCPressureValue", SubCycle=sub_cycle_id).id
            for sub_cycle_id in cycle.own
        ]

        self.state.bc_pressure_value_ids = bc_pressure_value_ids
        self.state.flush()


def initialize(server):
    state, ctrl = server.state, server.controller
    BCLogic(state, ctrl)
