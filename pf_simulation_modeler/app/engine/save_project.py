from .files import FileDatabase
from pathlib import Path
import os


def initialize(server):
    state, ctrl = server.state, server.controller

    state.save_dialog = False
    state.save_page = 1
    state.success_snackbar = False

    def save_project():
        state.success_snackbar = True

        output_dir = state.output_directory
        os.makedirs(output_dir, exist_ok=True)

        # Save python file
        code = ctrl.generate_code()
        code_file = Path(output_dir, state.sim_name + ".py")
        with open(code_file, "w") as f:
            f.write(code)

        # Save binary files
        file_database = FileDatabase()

        if state.indicator_file:
            indicator = file_database.getEntryData(state.indicator_file)
            indicator_file = Path(output_dir, state.indicator_filename)
            with open(indicator_file, "wb") as f:
                f.write(indicator)

        if state.slope_x_file:
            slope_x = file_database.getEntryData(state.slope_x_file)
            slope_x_file = Path(output_dir, state.slope_x_filename)
            with open(slope_x_file, "wb") as f:
                f.write(slope_x)

        if state.slope_y_file:
            slope_y = file_database.getEntryData(state.slope_y_file)
            slope_y_file = Path(output_dir, state.slope_y_filename)
            with open(slope_y_file, "wb") as f:
                f.write(slope_y)

        if state.pressure_file:
            pressure = file_database.getEntryData(state.pressure_file)
            pressure_file = Path(output_dir, state.pressure_filename)
            with open(pressure_file, "wb") as f:
                f.write(pressure)

        if state.elevation_file:
            elevation = file_database.getEntryData(state.elevation_file)
            elevation_file = Path(output_dir, state.elevation_filename)
            with open(elevation_file, "wb") as f:
                f.write(elevation)

        save_readme()

        state.save_dialog = False

    def save_readme():
        output_dir = state.output_directory
        os.makedirs(output_dir, exist_ok=True)

        source_file = Path(__file__, "..", "model", "output_readme.md").resolve()
        with open(source_file, "r") as f:
            readme = f.read()
        readme = readme.replace("{project_name}", state.sim_name)

        readme_file = Path(output_dir, "README.md")
        with open(readme_file, "w") as f:
            f.write(readme)

    @state.change("sim_name")
    def update_output_directory(sim_name, **kwargs):
        state.output_directory = str(Path(state.work_dir, sim_name).resolve())

    update_output_directory(state.sim_name)  # initialize output_directory

    ctrl.save_project = save_project
