import sys

from trame import state
from parflow import Run
from io import StringIO

from .files import FileDatabase
from .simput import KeyDatabase
from .io import (
    DefaultsIO, SoilIO, TimingIO, GridIO, CycleIO, BoundaryIO,
)

class ReplaceStdout(object):
    """
    A context manager to temporarely replace stdout
    """
    def __init__(self, stdout):
        self._original_stdout = sys.stdout
        self._replaced_stdout = stdout
        sys.stdout = stdout
    def __enter__(self):
        return self._replaced_stdout
    def __exit__(self, type, value, traceback):
        sys.stdout = self._original_stdout
        return True

def create_run(name="Simulation"):
    run = Run(name)

    DefaultsIO.write(run)

    pxm = KeyDatabase().pxm

    grid = pxm.get(state.gridId)
    GridIO.write(run, proxy=grid)

    timing = pxm.get(state.timingId)
    TimingIO.write(run, proxy=timing)

    for soil_id in state.soilIds:
        soil = pxm.get(soil_id)
        SoilIO.write(run, proxy=soil)

    for cycle_id in state.cycleIds:
        cycle = pxm.get(cycle_id)
        CycleIO.write(run, proxy=cycle, pxm=KeyDatabase().pxm)

    for boundary_id in state.BCPressureIds:
        boundary = pxm.get(boundary_id)
        BoundaryIO.write(
            run, proxy=boundary,
            value_ids=state.BCPressureValueIds.get(boundary_id, {}),
            pxm=KeyDatabase().pxm
        )

    return run

def validate_run():
    valid = False
    output = ""

    try:
        run = create_run("PF_Simulation_Modeler")

        with ReplaceStdout(StringIO()) as stdout:
            valid = run.validate() == 0

            if valid:
                print("Validation passed.")

            output = stdout.getvalue()

    except Exception:
        output = "Error Converting App State to Parflow Run."
        valid = False

    state.projGenValidation = {"output": output, "valid": valid}
