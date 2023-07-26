class DomainBuilderSnippet:
    def __init__(self, state):
        self.state = state

    def snippet(self, params):
        if not params:
            return ""

        # Domain
        origin = params.get("origin")
        spacing = params.get("spacing")
        size = params.get("size")

        slope_x = params.get("slope_x")
        slope_y = params.get("slope_y")

        # Simulation Type
        wells = params.get("wells")
        contaminants = params.get("contaminants")
        variably_saturated = params.get("saturated") == "Variably Saturated"

        # Boundary Conditions
        patches = params.get("patches")
        zero_flux = params.get("zero_flux")

        if not all([origin, spacing, size, slope_x, slope_y, patches, zero_flux]):
            return ""

        zero_flux_patches = ""
        zero_flux_code = []
        for (cycle, subcycle), group in zero_flux.items():
            zero_flux_patches += f"{group['name']} = '{group['patches']}'\n"
            zero_flux_code.append(
                f"    .zero_flux({group['name']}, '{cycle}', '{subcycle}') \\"
            )

        code = "# ------------------------------\n"
        code += "# Domain Builder\n"
        code += "# ------------------------------\n"
        code += zero_flux_patches + "\n"
        code += f"DomainBuilder({self.state.sim_name}) \\\n"
        if not wells:
            code += "    .no_wells() \\\n"
        if not contaminants:
            code += "    .no_contaminants() \\\n"
        if variably_saturated:
            code += "    .variably_saturated() \\\n"
        else:
            code += "    .fully_saturated() \\\n"
        code += "    .water('domain') \\\n"
        code += f"    .box_domain('{self.state.domain_geom_name}', 'domain', bounds, domain_patches) \\\n"
        code += "    .homogeneous_subsurface('domain', specific_storage=1.0e-5, isotropic=True) \\\n"
        code += "\n".join(zero_flux_code) + "\n"
        code += f"    .slopes_mannings('domain', slope_x='{slope_x}', slope_y='{slope_y}', mannings=5.52e-6) \\\n"
        code += f"    .ic_pressure('domain', patch='{self.state.pressure_patch}', pressure='{self.state.pressure_filename}')\n"
        return code
