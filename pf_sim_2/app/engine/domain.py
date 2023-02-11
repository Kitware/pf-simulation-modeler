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
                "domainView": "grid",
                "soils": [],
                "currentSoil": "all",
                "indicatorFile": None,
                "indicatorFileName": None,
                "slopeXFile": None,
                "slopeYFile": None,
                "elevationFile": None,
                "soilIds": [],
                "domainId": self.pxm.create("Domain").id,
                "gridId": grid_proxy.id,
                "bounds_id": self.pxm.create("Bounds").id,
                "patches_id": self.pxm.create("Patches").id,
            }
        )

    def update_bounds(self, topic, **kwargs):
        if topic != "update":
            return

        proxy: Proxy = self.pxm.get(self.state.gridId)
        if not proxy:
            return

        origin = proxy.get_property("Origin")
        spacing = proxy.get_property("Spacing")
        size = proxy.get_property("Size")

        if not all([origin, spacing, size]):
            return

        x_bound = origin[0] + spacing[0] * size[0]
        y_bound = origin[1] + spacing[1] * size[1]
        z_bound = origin[2] + spacing[2] * size[2]

        proxy: Proxy = self.pxm.get(self.state.bounds_id)
        if not proxy:
            return
        proxy.set_property("XBound", x_bound)
        proxy.set_property("YBound", y_bound)
        proxy.set_property("ZBound", z_bound)

    def updateComputationalGrid(self, indicatorFile, **kwargs):
        file_database = FileDatabase()

        if not indicatorFile:
            return

        entry = file_database.getEntry(indicatorFile)
        self.state.indicatorFileName = entry.get("origin")

        filename = file_database.getEntryPath(indicatorFile)
        try:
            handle = PFData(filename)
        except Exception as e:
            print(f"Could not find pfb: {filename}")
            raise e
        handle.loadHeader()

        change_set = [
            {
                "id": self.state.gridId,
                "name": "Origin",
                "value": [handle.getX(), handle.getY(), handle.getZ()],
            },
            {
                "id": self.state.gridId,
                "name": "Spacing",
                "value": [handle.getDX(), handle.getDY(), handle.getDZ()],
            },
            {
                "id": self.state.gridId,
                "name": "Size",
                "value": [handle.getNX(), handle.getNY(), handle.getNZ()],
            },
        ]
        self.pxm.update(change_set)

        for soilId in self.state.soilIds:
            self.pxm.delete(soilId)

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

        self.state.soilIds = soil_ids


def initialize(server):
    state, ctrl = server.state, server.controller

    domain_logic = DomainLogic(state, ctrl)

    @state.change("indicatorFile")
    def updateComputationalGrid(indicatorFile, **kwargs):
        domain_logic.updateComputationalGrid(indicatorFile)
