from trame_simput.core.proxy import Proxy


class SubsurfacePropertiesSnippet:
    def __init__(self, state, ctrl):
        self.state, self.ctrl = state, ctrl
        self.pxm = self.ctrl.get_pxm()

        self.soil_name_code = ""
        self.soil_code = ""

    def set_soil_names(self):
        soils = []
        for soild_id in self.state.soil_ids:
            proxy = self.pxm.get(soild_id)
            if not proxy:
                continue

            soils.append((proxy.get_property("key"), proxy.get_property("Value")))

        soil_list = " ".join([key for (key, _) in soils])
        code = f"{self.state.sim_name}.GeomInput.{self.state.indicator_geom_name}.GeomNames = '{soil_list}'"

        for key, value in soils:
            code += f"\n{self.state.sim_name}.GeomInput.{key}.Value = {value}"

        self.soil_name_code = code + "\n"

    def set_soils(self):
        props = [k for k in self.pxm.get_definition("Soil").keys() if k != "Value"]
        table_len = [len(prop) for prop in props]

        soils = []
        for soil_id in [self.state.domain_id, *self.state.soil_ids]:
            proxy: Proxy = self.pxm.get(soil_id)
            if not proxy:
                continue

            values = {}
            for i, prop in enumerate(props):
                value = proxy.get_property(prop)

                if value is None:
                    value = "-"
                if soil_id == self.state.domain_id and prop == "key":
                    value = "domain"

                values[prop] = value

                table_len[i] = max(table_len[i], len(str(value)))
            soils.append(values)

        table_len = [t + 2 for t in table_len]

        code = "subsurface_properties = '''\n"
        # Generate the headers for the columns
        line = ""
        for i, prop in enumerate(props):
            line += prop.ljust(table_len[i])
        code += line.strip() + "\n"

        # Populate the values for each soil
        for soil in soils:
            line = ""
            for i, prop in enumerate(props):
                line += str(soil[prop]).ljust(table_len[i])
            code += line.strip() + "\n"

        code += "'''\n\n"
        code += "# Setting subsurface properties\n"
        code += f"SubsurfacePropertiesBuilder({self.state.sim_name}) \\\n"
        code += "    .load_txt_content(subsurface_properties) \\\n"
        code += "    .apply()\n"

        self.soil_code = code

    @property
    def header(self):
        header = "# ------------------------------\n"
        header += "# Subsurface properties\n"
        header += "# ------------------------------\n"
        return header

    @property
    def snippet(self):
        self.set_soil_names()
        self.set_soils()
        return self.header + self.soil_name_code + "\n" + self.soil_code
