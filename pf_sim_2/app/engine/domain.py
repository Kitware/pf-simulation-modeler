from trame_simput.core.proxy import Proxy
from parflowio.pyParflowio import PFData
from .files import FileDatabase


class DomainLogic:
    def __init__(self, state, ctrl):
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

        grid_proxy: Proxy = self.pxm.create("ComputationalGrid")
        grid_proxy.on(self.update_bounds)

        state.update(
            {
                "domain_view": "grid",
                "soils": [],
                "current_soil": "all",
                "indicator_file": None,
                "indicator_filename": None,
                "slope_x_file": None,
                "slope_y_file": None,
                "elevation_file": None,
                "soil_ids": [],
                "domain_id": self.pxm.create("Domain").id,
                "grid_id": grid_proxy.id,
                "bounds_id": self.pxm.create("Bounds").id,
                "patches_id": self.pxm.create("Patches").id,
            }
        )

    def update_bounds(self, topic, **kwargs):
        if topic != "update":
            return

        proxy: Proxy = self.pxm.get(self.state.grid_id)
        if not proxy:
            return

        origin = proxy.get_property("Origin")
        spacing = proxy.get_property("Spacing")
        size = proxy.get_property("Size")

        if not all([origin, spacing, size]):
            return

        x_bound = [origin[0], origin[0] + spacing[0] * size[0]]
        y_bound = [origin[1], origin[1] + spacing[1] * size[1]]
        z_bound = [origin[2], origin[2] + spacing[2] * size[2]]

        proxy: Proxy = self.pxm.get(self.state.bounds_id)
        if not proxy:
            return
        proxy.set_property("XBound", x_bound)
        proxy.set_property("YBound", y_bound)
        proxy.set_property("ZBound", z_bound)
        proxy.commit()
        self.ctrl.simput_push(id=proxy.id)

    def updateComputationalGrid(self, indicator_file, **kwargs):
        file_database = FileDatabase()

        if not indicator_file:
            return

        entry = file_database.getEntry(indicator_file)
        self.state.indicator_filename = entry.get("origin")

        filename = file_database.getEntryPath(indicator_file)
        try:
            handle = PFData(filename)
        except Exception as e:
            print(f"Could not find pfb: {filename}")
            raise e
        handle.loadHeader()

        change_set = [
            {
                "id": self.state.grid_id,
                "name": "Origin",
                "value": [handle.getX(), handle.getY(), handle.getZ()],
            },
            {
                "id": self.state.grid_id,
                "name": "Spacing",
                "value": [handle.getDX(), handle.getDY(), handle.getDZ()],
            },
            {
                "id": self.state.grid_id,
                "name": "Size",
                "value": [handle.getNX(), handle.getNY(), handle.getNZ()],
            },
        ]
        self.pxm.update(change_set)

        for soil_id in self.state.soil_ids:
            self.pxm.delete(soil_id)

        handle.loadData()
        data = handle.viewDataArray()

        unique_values = set()
        for val in data.flat:
            unique_values.add(round(val))

        handle.close()

        soil_ids = []
        for val in unique_values:
            soil = self.pxm.create("Soil", **{"key": f"s{val}", "Value": val})
            soil_ids.append(soil.id)

        self.state.soil_ids = soil_ids


def initialize(server):
    state, ctrl = server.state, server.controller

    domain_logic = DomainLogic(state, ctrl)

    @state.change("indicator_file")
    def updateComputationalGrid(indicator_file, **kwargs):
        domain_logic.updateComputationalGrid(indicator_file)
