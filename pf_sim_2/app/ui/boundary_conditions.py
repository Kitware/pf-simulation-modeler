from trame.widgets import vuetify, html, simput
from functools import partial


class BoundaryConditions:
    def __init__(self, server):
        state, ctrl = server.state, server.controller
        self.server = server
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

        patches = ["x_lower", "x_upper", "y_lower", "y_upper", "z_lower", "z_upper"]
        bc_pressures = list(
            map(lambda patch: self.pxm.create("BCPressure", Patch=patch), patches)
        )
        for bcp in bc_pressures:
            bcp.on(partial(self.on_bcp_change, bcp.id))

        bc_pressure_ids = list(map(lambda bcp: bcp.id, bc_pressures))

        state.update(
            {
                "BCPressureIds": bc_pressure_ids,
                "BCPressureValueIds": {},
            }
        )

    def on_bcp_change(self, id, topic, **kwargs):
        if topic != "update" and kwargs.get("property_name") != "Cycle":
            return

        bcp = self.pxm.get(id)
        cycle_id = bcp["Cycle"]

        cycle = self.pxm.get(cycle_id)

        # Delete values defined for other cycles
        for value_id in self.state.BCPressureValueIds.get(id, []):
            self.pxm.delete(value_id)

        # Create new values for the new cycle
        self.state.BCPressureValueIds[id] = [
            self.pxm.create("BCPressureValue", SubCycle=sub_cycle_id).id
            for sub_cycle_id in cycle.own
        ]

        self.state.flush("BCPressureValueIds")

    def page(self):
        html.H1("Boundary Conditions")

        with vuetify.VContainer(v_for=("(id, i) in BCPressureIds",), fluid=True):
            simput.SimputItem(item_id=("id",))
            with vuetify.VContainer(fluid=True, style="padding: 3rem;"):
                simput.SimputItem(
                    v_for=("(valueId, vi) in BCPressureValueIds[id]",),
                    item_id=("valueId",),
                )
