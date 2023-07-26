from trame_simput.core.proxy import Proxy


class TimingSnippet:
    def __init__(self, state, ctrl):
        self.state, self.ctrl = state, ctrl
        self.pxm = self.ctrl.get_pxm()

        self.timing_info_code = ""
        self.time_cycle_code = ""

    def set_timing_info(self):
        proxy: Proxy = self.pxm.get(self.state.timing_id)
        if not proxy:
            return

        code = f"{self.state.sim_name}.TimingInfo.BaseUnit = {proxy.get_property('BaseUnit')}\n"
        code += f"{self.state.sim_name}.TimingInfo.StartCount = {proxy.get_property('StartCount')}\n"
        code += f"{self.state.sim_name}.TimingInfo.StartTime = {proxy.get_property('StartTime')}\n"
        code += f"{self.state.sim_name}.TimingInfo.StopTime = {proxy.get_property('StopTime')}\n"
        code += f"{self.state.sim_name}.TimingInfo.DumpInterval = {proxy.get_property('DumpInterval')}\n"
        code += f"{self.state.sim_name}.TimeStep.Type = 'Constant'\n"
        code += f"{self.state.sim_name}.TimeStep.Value = 1.0\n"

        self.timing_info_code = code

    def set_cycles(self):
        cycles = []
        names = []
        for cycle_id in self.state.cycle_ids:
            proxy: Proxy = self.pxm.get(cycle_id)
            if not proxy:
                continue

            name = proxy.get_property("Name")
            repeat = proxy.get_property("Repeat")

            subcycles = []
            for subcycle_id in proxy.own:
                proxy: Proxy = self.pxm.get(subcycle_id)
                if not proxy:
                    continue

                subcycles.append(
                    {
                        "name": proxy.get_property("Name"),
                        "length": proxy.get_property("Length"),
                    }
                )

            cycles.append({"name": name, "repeat": repeat, "subcycles": subcycles})
            names.append(name)

        code = f"{self.state.sim_name}.Cycle.Names = '{' '.join(names)}'\n\n"
        for cycle in cycles:
            code += f"{self.state.sim_name}.Cycle.{cycle['name']}.Names = '{' '.join(sub['name'] for sub in cycle['subcycles'])}'\n"
            code += f"{self.state.sim_name}.Cycle.{cycle['name']}.Repeat = {cycle['repeat']}\n"

            for subcycle in cycle["subcycles"]:
                code += f"{self.state.sim_name}.Cycle.{cycle['name']}.{subcycle['name']}.Length = {subcycle['length']}\n"
            code += "\n"

        self.time_cycle_code = code

    @property
    def header(self):
        header = "# ------------------------------\n"
        header += "# Timing\n"
        header += "# ------------------------------"
        return header

    @property
    def snippet(self):
        self.set_timing_info()
        self.set_cycles()
        code = [self.header, self.timing_info_code, self.time_cycle_code]
        return "\n".join([s for s in code if s])
