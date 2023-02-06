from parflowio.pyParflowio import PFData
from .files import FileDatabase


class DomainLogic:
    def __init__(self, state, ctrl):
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

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
                "gridId": self.pxm.create("ComputationalGrid").id,
            }
        )

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
