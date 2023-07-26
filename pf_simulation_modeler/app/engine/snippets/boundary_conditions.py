from trame_simput.core.proxy import Proxy


class BoundaryConditionsSnippet:
    def __init__(self, state, ctrl):
        self.state, self.ctrl = state, ctrl
        self.pxm = self.ctrl.get_pxm()

        self.patches = []
        self.zero_flux = {}
        self.other_flux = {}

        self.bc_explicit_code = ""

        self.domain_builder_params = {}

    # Collect pressure cycles for all patches
    def _get_patch_pressures(self):
        pressures = []
        cycle_subcycle_pairs = set()
        self.patches = []

        for id in self.state.bc_pressure_ids:
            proxy: Proxy = self.pxm.get(id)
            if not proxy:
                continue

            p_patch = proxy.get_property("Patch")
            p_type = proxy.get_property("Type")
            p_cycle = proxy.get_property("Cycle")
            p_cycle = self.state.cycle_defs.get(p_cycle, p_cycle)

            p_subcycle = {}
            for value_id in self.state.bc_pressure_value_ids.get(id, []):
                proxy: Proxy = self.pxm.get(value_id)
                if not proxy:
                    continue

                subcycle = proxy.get_property("SubCycle")
                subcycle = self.state.subcycle_defs.get(subcycle, subcycle)
                value = proxy.get_property("Value")

                p_subcycle[subcycle] = value

                cycle_subcycle_pairs.add((p_cycle, subcycle))

            pressures.append((p_patch, p_type, p_cycle, p_subcycle))
            self.patches.append(p_patch)

        return pressures, cycle_subcycle_pairs

    # Categorize patches belonging to zero_flux and patches that don't
    def _categorize_flux_groups(self):
        # Get pressure cycle data from simput items
        pressures, cycle_subcycle_pairs = self._get_patch_pressures()

        zero_flux = {}
        other_flux = {}

        for cycle, interval in cycle_subcycle_pairs:
            if not cycle or not interval:
                continue

            for pressure in pressures:
                p_patch, p_type, p_cycle, p_subcycle = pressure

                if p_cycle != cycle or interval not in p_subcycle.keys():
                    continue

                if p_type != "FluxConst" or len(p_subcycle) > 1:
                    # Not suitable for zero_flux
                    other_flux[p_patch] = pressure
                    continue

                for subcycle, value in p_subcycle.items():
                    if subcycle != interval:
                        continue

                    if value != 0:
                        # Not suitable for zero_flux
                        other_flux[p_patch] = pressure
                        continue

                    if (cycle, interval) not in zero_flux:
                        zero_flux[(cycle, interval)] = []
                    zero_flux[(cycle, interval)].append(pressure)

        return zero_flux, other_flux

    def set_boundary_conditions(self):
        # Categorize patches into zero_flux and other_flux groups
        self.zero_flux, self.other_flux = self._categorize_flux_groups()

        zero_flux_patches_code = {}
        for (cycle, subcycle), patches in self.zero_flux.items():
            if len(self.zero_flux) == 1:
                name = "zero_flux_patches"
            else:
                name = f"zero_flux_{cycle}_{subcycle}_patches"

            patch_list = " ".join([patch[0] for patch in patches])
            zero_flux_patches_code[(cycle, subcycle)] = {
                "name": name,
                "patches": patch_list,
            }

        self.domain_builder_params["zero_flux"] = zero_flux_patches_code
        self.domain_builder_params["patches"] = self.patches

        # Generate explicit BCPressure info for non-zero_flux patches
        patches = []
        for p_patch, p_type, p_cycle, p_subcycle in self.other_flux.values():
            code = f"# {p_patch}\n"
            code += (
                f"{self.state.sim_name}.Patch.{p_patch}.BCPressure.Type = '{p_type}'\n"
            )
            code += f"{self.state.sim_name}.Patch.{p_patch}.BCPressure.Cycle = '{p_cycle}'\n"

            for subcycle, value in p_subcycle.items():
                if value is None:
                    continue
                code += f"{self.state.sim_name}.Patch.{p_patch}.BCPressure.{subcycle}.Value = {value}\n"

            patches.append(code)

        code = "# ------------------------------\n"
        code += "# Boundary Conditions\n"
        code += "# ------------------------------\n"
        code += f"{self.state.sim_name}.BCPressure.PatchNames = {self.state.sim_name}.Geom.domain.Patches\n"
        code += "\n".join(patches)
        self.bc_explicit_code = code

    @property
    def snippet(self):
        self.set_boundary_conditions()
        return self.bc_explicit_code
