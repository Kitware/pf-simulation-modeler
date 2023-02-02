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

        return "\n".join(
            [
                "bounds = [",
                f"    {origin[0]}, {origin[0] + (spacing[0] * size[0])},",
                f"    {origin[1]}, {origin[1] + (spacing[1] * size[1])},",
                f"    {origin[2]}, {origin[2] + (spacing[2] * size[2])}",
                "]",
                "",
                f"domain_patches = '{' '.join(patches)}'",
                zero_flux_patches,
                "",
                "DomainBuilder(LW_Test) \\",
                "    .no_wells() \\" if not wells else "    \\",
                "    .no_contaminants() \\" if not contaminants else "    \\",
                "    .variably_saturated() \\"
                if variably_saturated
                else "    .fully_saturated() \\",
                "    .water('domain') \\",
                "    .box_domain('box_input', 'domain', bounds, domain_patches) \\",
                "    .homogeneous_subsurface('domain', specific_storage=1.0e-5, isotropic=True) \\",
                "\n".join(zero_flux_code),
                f"    .slopes_mannings('domain', slope_x='{slope_x}', slope_y='{slope_y}', mannings=5.52e-6) \\",
                "    .ic_pressure('domain', patch='z_upper', pressure='press.init.pfb')",
            ]
        )
