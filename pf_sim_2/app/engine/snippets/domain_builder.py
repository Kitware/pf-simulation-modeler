class DomainBuilderSnippet:
    def snippet(self, domain_builder_params):
        if not domain_builder_params:
            return ""

        origin = domain_builder_params.get("origin")
        spacing = domain_builder_params.get("spacing")
        size = domain_builder_params.get("size")

        slope_x = domain_builder_params.get("slope_x")
        slope_y = domain_builder_params.get("slope_y")

        wells = domain_builder_params.get("wells")
        contaminants = domain_builder_params.get("contaminants")
        variably_saturated = (
            domain_builder_params.get("saturated") == "Variably Saturated"
        )

        if not all([origin, spacing, size, slope_x, slope_y]):
            return ""

        return "\n".join(
            [
                "bounds = [",
                f"    {origin[0]}, {origin[0] + (spacing[0] * size[0])},",
                f"    {origin[1]}, {origin[1] + (spacing[1] * size[1])},",
                f"    {origin[2]}, {origin[2] + (spacing[2] * size[2])}",
                "]",
                "",
                "domain_patches = 'x_lower x_upper y_lower y_upper z_lower z_upper'",
                "zero_flux_patches = 'x_lower x_upper y_lower y_upper z_lower'",
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
                f"    .zero_flux(zero_flux_patches, '{'constant'}', '{'alltime'}') \\",
                f"    .slopes_mannings('domain', slope_x='{slope_x}', slope_y='{slope_y}', mannings=5.52e-6) \\",
                "    .ic_pressure('domain', patch='z_upper', pressure='press.init.pfb')",
            ]
        )
