from trame_simput.core.proxy import Proxy


class SubsurfacePropertiesSnippet:
    def __init__(self, state, ctrl):
        self.state, self.ctrl = state, ctrl
        self.pxm = self.ctrl.get_pxm()

        self.code = ""

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
        code += "SubsurfacePropertiesBuilder(LW_Test) \\\n"
        code += "    .load_txt_content(subsurface_properties) \\\n"
        code += "    .apply()\n"

        self.code = code

    @property
    def header(self):
        header = "# ------------------------------\n"
        header += "# Subsurface properties\n"
        header += "# ------------------------------\n"
        return header

    @property
    def snippet(self):
        return self.header + self.code
