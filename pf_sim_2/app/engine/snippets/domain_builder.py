class DomainBuilderSnippet:
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
        code += "bounds = [\n"
        code += f"    {origin[0]}, {origin[0] + (spacing[0] * size[0])},\n"
        code += f"    {origin[1]}, {origin[1] + (spacing[1] * size[1])},\n"
        code += f"    {origin[2]}, {origin[2] + (spacing[2] * size[2])}\n"
        code += "]\n\n"
        code += f"domain_patches = '{' '.join(patches)}'\n"
        code += zero_flux_patches + "\n"
        code += "DomainBuilder(LW_Test) \\\n"
        if not wells:
            code += "    .no_wells() \\\n"
        if not contaminants:
            code += "    .no_contaminants() \\\n"
        if variably_saturated:
            code += "    .variably_saturated() \\\n"
        else:
            code += "    .fully_saturated() \\\n"
        code += "    .water('domain') \\\n"
        code += "    .box_domain('box_input', 'domain', bounds, domain_patches) \\\n"
        code += "    .homogeneous_subsurface('domain', specific_storage=1.0e-5, isotropic=True) \\\n"
        code += "\n".join(zero_flux_code) + "\n"
        code += f"    .slopes_mannings('domain', slope_x='{slope_x}', slope_y='{slope_y}', mannings=5.52e-6) \\\n"
        code += (
            "    .ic_pressure('domain', patch='z_upper', pressure='press.init.pfb')\n"
        )
        return code
