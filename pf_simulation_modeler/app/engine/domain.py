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
                "soil_ids": [],
                "current_soil": "all",
                # Files
                "indicator_file": None,
                "slope_x_file": None,
                "slope_y_file": None,
                "elevation_file": None,
                "indicator_filename": None,
                "slope_x_filename": None,
                "slope_y_filename": None,
                "elevation_filename": None,
                # Simput
                "domain_id": self.pxm.create("Domain").id,
                "grid_id": grid_proxy.id,
                "patches_id": self.pxm.create("Patches").id,
                # Bounds
                "x_bound": ["", ""],
                "y_bound": ["", ""],
                "z_bound": ["", ""],
                "domain_geom_name": "box_input",
                "indicator_geom_name": "indi_input",
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

        self.state.x_bound = [origin[0], origin[0] + spacing[0] * size[0]]
        self.state.y_bound = [origin[1], origin[1] + spacing[1] * size[1]]
        self.state.z_bound = [origin[2], origin[2] + spacing[2] * size[2]]

    def update_indicator(self, indicator_file, **kwargs):
        file_database = FileDatabase()

        if not indicator_file:
            return

        entry = file_database.getEntry(indicator_file)
        self.state.indicator_filename = entry.get("origin")

        self.state.indicator_geom_name = "".join(
            self.state.indicator_filename.split(".")[:-1]
        )

        # extract soil data from pfb
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

    def update_slope_x(self, slope_x_file, **kwargs):
        if not slope_x_file:
            return

        file_database = FileDatabase()
        entry = file_database.getEntry(slope_x_file)
        self.state.slope_x_filename = entry.get("origin")

    def update_slope_y(self, slope_y_file, **kwargs):
        if not slope_y_file:
            return

        file_database = FileDatabase()
        entry = file_database.getEntry(slope_y_file)
        self.state.slope_y_filename = entry.get("origin")

    def update_elevation(self, elevation_file, **kwargs):
        if not elevation_file:
            return

        file_database = FileDatabase()
        entry = file_database.getEntry(elevation_file)
        self.state.elevation_filename = entry.get("origin")


def initialize(server):
    state, ctrl = server.state, server.controller

    domain_logic = DomainLogic(state, ctrl)

    state.change("indicator_file")(domain_logic.update_indicator)
    state.change("slope_x_file")(domain_logic.update_slope_x)
    state.change("slope_y_file")(domain_logic.update_slope_y)
    state.change("elevation_file")(domain_logic.update_elevation)
