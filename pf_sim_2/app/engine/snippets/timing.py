from trame_simput.core.proxy import Proxy


class TimingSnippet:
    def __init__(self, state, ctrl):
        self.state, self.ctrl = state, ctrl
        self.pxm = self.ctrl.get_pxm()

        self.timing_info_code = ""
        self.time_cycle_code = ""

    def set_timing_info(self):
        proxy: Proxy = self.pxm.get(self.state.timingId)
        if not proxy:
            return

        self.timing_info_code = "\n".join(
            [
                f"LW_Test.TimingInfo.BaseUnit = {proxy.get_property('BaseUnit')}",
                f"LW_Test.TimingInfo.StartCount = {proxy.get_property('StartCount')}",
                f"LW_Test.TimingInfo.StartTime = {proxy.get_property('StartTime')}",
                f"LW_Test.TimingInfo.StopTime = {proxy.get_property('StopTime')}",
                f"LW_Test.TimingInfo.DumpInterval = {proxy.get_property('DumpInterval')}",
            ]
        )

    def set_cycles(self):
        cycles = []
        names = []
        for cycle_id in self.state.cycleIds:
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

        code = f"LW_Test.Cycle.Names = '{' '.join(names)}'\n\n"
        for cycle in cycles:
            code += f"LW_Test.Cycle.{cycle['name']}.Names = '{' '.join(sub['name'] for sub in cycle['subcycles'])}'\n"
            code += f"LW_Test.Cycle.{cycle['name']}.Repeat = {cycle['repeat']}\n"

            for subcycle in cycle["subcycles"]:
                code += f"LW_Test.Cycle.{cycle['name']}.{subcycle['name']}.Length = {subcycle['length']}\n"
            code += "\n"

        self.time_cycle_code = code

    @property
    def snippet(self):
        return "\n\n".join([self.timing_info_code, self.time_cycle_code])
