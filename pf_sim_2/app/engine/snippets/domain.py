from trame_simput.core.proxy import Proxy
from ..files import FileDatabase


class DomainSnippet:
    def __init__(self, state, ctrl):
        self.state, self.ctrl = state, ctrl
        self.pxm = self.ctrl.get_pxm()

        self.indicator_code = ""
        self.grid_code = ""
        self.soil_code = ""
        self.patches_code = ""

        self.domain_builder_params = {}

    def set_grid(self):
        proxy = self.pxm.get(self.state.grid_id)
        if not proxy:
            return

        origin = proxy.get_property("Origin")
        spacing = proxy.get_property("Spacing")
        size = proxy.get_property("Size")
        if not all([origin, spacing, size]):
            return

        code = f"{self.state.sim_name}.ComputationalGrid.Lower.X = {origin[0]}\n"
        code += f"{self.state.sim_name}.ComputationalGrid.Lower.Y = {origin[1]}\n"
        code += f"{self.state.sim_name}.ComputationalGrid.Lower.Z = {origin[2]}\n\n"
        code += f"{self.state.sim_name}.ComputationalGrid.DX = {spacing[0]}\n"
        code += f"{self.state.sim_name}.ComputationalGrid.DY = {spacing[1]}\n"
        code += f"{self.state.sim_name}.ComputationalGrid.DZ = {spacing[2]}\n\n"
        code += f"{self.state.sim_name}.ComputationalGrid.NX = {size[0]}\n"
        code += f"{self.state.sim_name}.ComputationalGrid.NY = {size[1]}\n"
        code += f"{self.state.sim_name}.ComputationalGrid.NZ = {size[2]}\n\n"
        code += "bounds = [\n"
        code += f"    {origin[0]}, {origin[0] + (spacing[0] * size[0])},\n"
        code += f"    {origin[1]}, {origin[1] + (spacing[1] * size[1])},\n"
        code += f"    {origin[2]}, {origin[2] + (spacing[2] * size[2])}\n"
        code += "]\n"
        self.grid_code = code

        self.domain_builder_params["origin"] = origin
        self.domain_builder_params["spacing"] = spacing
        self.domain_builder_params["size"] = size

    def set_patches(self):
        proxy: Proxy = self.pxm.get(self.state.patches_id)
        if not proxy:
            return

        code = "domain_patches = '"
        code += f"{proxy.get_property('XLower')} "
        code += f"{proxy.get_property('XUpper')} "
        code += f"{proxy.get_property('YLower')} "
        code += f"{proxy.get_property('YUpper')} "
        code += f"{proxy.get_property('ZLower')} "
        code += f"{proxy.get_property('ZUpper')}"
        code += "'\n"
        self.patches_code = code

    def set_terrain_files(self):
        file_database = FileDatabase()
        # Slope X
        entry = file_database.getEntry(self.state.slope_x_file)
        if not entry:
            return
        self.domain_builder_params["slope_x"] = entry.get("origin")

        # Slope Y
        entry = file_database.getEntry(self.state.slope_y_file)
        if not entry:
            return
        self.domain_builder_params["slope_y"] = entry.get("origin")

    def set_indicator_file(self):
        code = f"{self.state.sim_name}.GeomInput.Names = 'box_input indi_input'\n\n"
        code += (
            f"{self.state.sim_name}.GeomInput.indi_input.InputType = 'IndicatorField'\n"
        )
        code += f"{self.state.sim_name}.Geom.indi_input.FileName = '{self.state.indicator_filename}'\n"
        self.indicator_code = code

    def set_soils(self):
        soils = []
        for soild_id in self.state.soil_ids:
            proxy = self.pxm.get(soild_id)
            if not proxy:
                continue

            soils.append((proxy.get_property("key"), proxy.get_property("Value")))

        soil_list = " ".join([key for (key, _) in soils])
        self.soil_code = (
            f"{self.state.sim_name}.GeomInput.indi_input.GeomNames = '{soil_list}'"
        )

        for (key, value) in soils:
            self.soil_code += f"\n{self.state.sim_name}.GeomInput.{key}.Value = {value}"

    @property
    def header(self):
        header = "# ------------------------------\n"
        header += "# Domain\n"
        header += "# ------------------------------"
        return header

    @property
    def snippet(self):
        self.set_grid()
        self.set_patches()
        self.set_terrain_files()
        self.set_indicator_file()
        self.set_soils()
        return "\n".join(
            [
                self.header,
                self.grid_code,
                self.patches_code,
                self.indicator_code,
                self.soil_code,
                "",
            ]
        )
