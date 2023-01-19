class DomainSnippet:
    def __init__(self, state, ctrl):
        self.state, self.ctrl = state, ctrl
        self.pxm = self.ctrl.get_pxm()

        self.indicator_code = ""
        self.grid_code = ""
        self.soil_code = ""

        self.domain_builder_params = {}

    def set_indicator_file(self, indicator_file_name):
        if not indicator_file_name:
            return
        self.indicator_code = (
            "LW_Test.GeomInput.indi_input.InputType = 'IndicatorField'\n"
            + f"LW_Test.Geom.indi_input.FileName = '{indicator_file_name}'"
        )

    def set_grid(self, grid_id):
        proxy = self.pxm.get(grid_id)
        if not proxy:
            return

        origin = proxy.get_property("Origin")
        spacing = proxy.get_property("Spacing")
        size = proxy.get_property("Size")
        if not all([origin, spacing, size]):
            return

        self.grid_code = "\n".join(
            [
                f"LW_Test.ComputationalGrid.Lower.X = {origin[0]}",
                f"LW_Test.ComputationalGrid.Lower.Y = {origin[1]}",
                f"LW_Test.ComputationalGrid.Lower.Z = {origin[2]}",
                "",
                f"LW_Test.ComputationalGrid.DX = {spacing[0]}",
                f"LW_Test.ComputationalGrid.DY = {spacing[1]}",
                f"LW_Test.ComputationalGrid.DZ = {spacing[2]}",
                "",
                f"LW_Test.ComputationalGrid.NX = {size[0]}",
                f"LW_Test.ComputationalGrid.NY = {size[1]}",
                f"LW_Test.ComputationalGrid.NZ = {size[2]}",
            ]
        )

        self.domain_builder_params["origin"] = origin
        self.domain_builder_params["spacing"] = spacing
        self.domain_builder_params["size"] = size

    def set_terrain_files(self, slope_x, slope_y):
        if not slope_x or not slope_y:
            return

        self.domain_builder_params["slope_x"] = slope_x
        self.domain_builder_params["slope_y"] = slope_y

    def set_soils(self, soil_ids):
        soils = []
        for soildId in soil_ids:
            proxy = self.pxm.get(soildId)
            if not proxy:
                continue

            soils.append((proxy.get_property("Key"), proxy.get_property("Value")))

        soil_list = " ".join([key for (key, _) in soils])
        self.soil_code = f"LW_Test.Geom.terrain_input.Soil_Values = '{soil_list}'"

        for (key, value) in soils:
            self.soil_code += f"\nLW_Test.GeomInput.{key}.Value = {value}"

    @property
    def snippet(self):
        return "\n\n".join([self.grid_code, self.indicator_code, self.soil_code])
