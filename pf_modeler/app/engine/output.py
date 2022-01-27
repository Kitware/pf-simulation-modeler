import sys
import os.path
import yaml

from trame import state
from parflow import Run
from io import StringIO

from .files import FileDatabase

defaults = {
    #
    # These require reading nested keys
    #
    "Cycle.constant.alltime.Length": 1,
    "Cycle.Names": "constant",
    "Cycle.constant.Names": "alltime",
    "Cycle.constant.Repeat": -1,
    "Patch.x_lower.BCPressure.alltime.Value": 0,
    "Patch.x_upper.BCPressure.alltime.Value": 0,
    "Patch.y_lower.BCPressure.alltime.Value": 0,
    "Patch.y_upper.BCPressure.alltime.Value": 0,
    "Patch.z_lower.BCPressure.alltime.Value": 0,
    "Patch.z_upper.BCPressure.alltime.Value": 0,
    "PhaseSources.water.Geom.domain.Value": 0,
    #
    # These require top level __value__ keys
    #
    "Gravity": 1.0,
    "FileVersion": 4,
    "KnownSolution": "NoKnownSolution",
    "Solver._value_": "Richards",
    #
    # These may be wrong in LW_Test.yaml. That key doesn't exist in pf-keys
    #
    "Solver.Linear.Preconditioner._value_": "PFMGOctree",
}


class RunWriter:
    def __init__(self, work_dir, filedb):
        self.work_dir = work_dir
        self.run = {}

    def read_from_simput(self):
        from . import key_database

        pxm = key_database.pxm
        extracted_keys = {}

        for proxy_type in pxm.types():
            definition = pxm.get_definition(proxy_type)
            for proxy in pxm.get_instances_of_type(proxy_type):
                for (prop_name, prop) in proxy.definition.items():
                    if prop_name == "name" or prop_name.startswith("_"):
                        continue
                    value = proxy.get_property(prop_name)
                    if value is not None:
                        if definition.get("_exportPrefix"):
                            name = ".".join(
                                [
                                    definition["_exportPrefix"],
                                    proxy.get_property("name"),
                                    prop["_exportSuffix"],
                                ]
                            )
                        else:
                            name = prop["_exportSuffix"]
                        extracted_keys[name] = value

        self.run.update(extracted_keys)
        self.run.update(defaults)

    def validate_run(self):
        self.read_from_simput()
        path = os.path.join(self.work_dir, "run.yaml")
        with open(path, "w") as runFile:
            yaml.dump(self.run, runFile)

        run = Run.from_definition(path)
        run.dist("IndicatorFile_Gleeson.50z.pfb")
        run.run()

        try:
            # Redirect stdout to capture validation msg
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            valid = run.validate() == 0

            if valid:
                print("Validation passed.")
        finally:
            sys.stdout = old_stdout

        return mystdout.getvalue()


def validate_run():
    parflow = RunWriter(state.work_dir, FileDatabase())
    validation = parflow.validate_run()

    state.projGenValidation = {"output": validation, "valid": False}
