from .files import FileDatabase


class PressureLogic:
    def __init__(self, state, ctrl):
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

        state.update(
            {
                # File
                "pressure_file": None,
                "pressure_filename": None,
                # Patches
                "pressure_patch": None,
            }
        )

    def update_pressure(self, pressure_file, **kwargs):
        if not pressure_file:
            return

        file_database = FileDatabase()
        entry = file_database.getEntry(pressure_file)
        self.state.pressure_filename = entry.get("origin")


def initialize(server):
    state, ctrl = server.state, server.controller

    pressure_logic = PressureLogic(state, ctrl)
    state.change("pressure_file")(pressure_logic.update_pressure)
