from functools import partial


class BCLogic:
    def __init__(self, state, ctrl):
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

        patches = ["x_lower", "x_upper", "y_lower", "y_upper", "z_lower", "z_upper"]
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
            }
        )

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
