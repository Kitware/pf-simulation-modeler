class TimingSnippet:
    def __init__(self, state, ctrl):
        self.state, self.ctrl = state, ctrl
        self.pxm = self.ctrl.get_pxm()
        self.timing_info_code = ""

    def set_timing_info(self, timing_id):
        if not timing_id:
            return

        proxy = self.pxm.get(timing_id)
        if not proxy:
            return
        print("timing_id", proxy.state)

        self.timing_info_code = "\n".join(
            [
                f"LW_Test.TimingInfo.BaseUnit = {proxy.get_property('BaseUnit')}",
                f"LW_Test.TimingInfo.StartCount = {proxy.get_property('StartCount')}",
                f"LW_Test.TimingInfo.StartTime = {proxy.get_property('StartTime')}",
                f"LW_Test.TimingInfo.StopTime = {proxy.get_property('StopTime')}",
                f"LW_Test.TimingInfo.DumpInterval = {proxy.get_property('DumpInterval')}",
            ]
        )

    @property
    def snippet(self):
        return "\n\n".join([self.timing_info_code])
