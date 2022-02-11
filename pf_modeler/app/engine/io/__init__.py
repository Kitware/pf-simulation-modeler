from parflow import Run

from abc import ABC, abstractmethod, abstractstaticmethod

"""
The internal state of the app is split across:
  - Trame state
  - Singletons
  - Simput proxies

In this module we have a set of methods to create a parflow Run
from the various pieces of the app state (and vice-versa).
"""

def get_item(proxy, key, default=None):
    try:
        value = proxy[key]
    except Exception:
        value = default

    return value

def value_or_default(value, default=None):
    if value is None:
        return default
    else:
        return value

class BaseIO(ABC):
    @staticmethod
    def write(run: Run, **kwargs):
        pass

    @staticmethod
    def read(run: Run, **kwargs):
        pass

class GridIO(BaseIO):
    @staticmethod
    def write(run: Run, proxy, **kwargs):
        origin = proxy["Origin"]
        spacing = proxy["Spacing"]
        size = proxy["Size"]

        run.ComputationalGrid.Lower.X = origin[0]
        run.ComputationalGrid.Lower.Y = origin[1]
        run.ComputationalGrid.Lower.Z = origin[2]

        run.ComputationalGrid.DX = spacing[0]
        run.ComputationalGrid.DY = spacing[1]
        run.ComputationalGrid.DZ = spacing[2]

        run.ComputationalGrid.NX = size[0]
        run.ComputationalGrid.NY = size[1]
        run.ComputationalGrid.NZ = size[2]

        # -----------------------------------------------------------------------------
        # Domain Geometry
        # -----------------------------------------------------------------------------

        run.Geom.domain.Lower.X = origin[0]
        run.Geom.domain.Lower.Y = origin[1]
        run.Geom.domain.Lower.Z = origin[2]
        #
        run.Geom.domain.Upper.X = origin[0] + spacing[0] * size[0]
        run.Geom.domain.Upper.Y = origin[1] + spacing[1] * size[1]
        run.Geom.domain.Upper.Z = origin[2] + spacing[2] * size[2]

class TimingIO(BaseIO):
    @staticmethod
    def write(run: Run, proxy, **kwargs):
        run.TimingInfo.BaseUnit = proxy["BaseUnit"]
        run.TimingInfo.StartCount = proxy["StartCount"]
        run.TimingInfo.StartTime = proxy["StartTime"]
        run.TimingInfo.StopTime = proxy["StopTime"]
        run.TimingInfo.DumpInterval = proxy["DumpInterval"]
        run.TimeStep.Type = "Constant"
        run.TimeStep.Value = 1.0

class SoilIO(BaseIO):
    @staticmethod
    def write(run: Run, proxy, **kwargs):
        key = proxy["Key"]

        value = get_item(proxy, "Value")

        if value is not None:
            curr = value_or_default(run.GeomInput.indi_input.GeomNames, [])
            run.GeomInput.indi_input.GeomNames = curr + [key]

            getattr(run.GeomInput, key).Value = value

        perm = get_item(proxy, "Perm")

        if perm is not None:
            curr = value_or_default(run.Geom.Perm.Names, [])
            run.Geom.Perm.Names = curr + [key]

            getattr(run.Geom, key).Perm.Type = "Constant"
            getattr(run.Geom, key).Perm.Value = perm

class CycleIO(BaseIO):
    @staticmethod
    def write(run: Run, proxy, pxm, **kwargs):
        name = proxy["Name"]
        curr = value_or_default(run.Cycle.Names, [])
        run.Cycle.Names = curr + [name]

        getattr(run.Cycle, name).Repeat = proxy["Repeat"]

        sub_names = []
        sub_lengths = []
        for id in proxy.own:
            sub_cycle = pxm.get(id)
            sub_names.append(sub_cycle["Name"])
            sub_lengths.append(sub_cycle["Length"])

        getattr(run.Cycle, name).Names = sub_names

        for sub_name, length in zip(sub_names, sub_lengths):
            getattr(getattr(run.Cycle, name), sub_name).Length = length

class BoundaryIO(BaseIO):
    @staticmethod
    def write(run: Run, proxy, value_ids, pxm, **kwargs):
        patch = proxy["Patch"]

        curr = value_or_default(run.BCPressure.PatchNames, [])
        run.BCPressure.PatchNames = curr + [patch]

        curr = value_or_default(run.BCPressure.PatchNames, [])
        run.BCPressure.PatchNames = curr + [patch]

        getattr(run.Patch, patch).BCPressure.Type = proxy["Type"]

        cycle_id = proxy["Cycle"]
        cycle = pxm.get(cycle_id)

        getattr(run.Patch, patch).BCPressure.Cycle = cycle["Name"]

        for value_id in value_ids:
            bcp_value = pxm.get(value_id)
            sub_cycle_id = bcp_value["SubCycle"]
            sub_cycle = pxm.get(sub_cycle_id)
            getattr(getattr(run.Patch, patch).BCPressure, sub_cycle["Name"]).Value = bcp_value["Value"]


class DefaultsIO(BaseIO):
    @staticmethod
    def write(run: Run, **kwargs):
        """Defaults that are not exposed to the user"""
        run.FileVersion = 4

        run.Process.Topology.P = 1
        run.Process.Topology.Q = 1
        run.Process.Topology.R = 1

        # -----------------------------------------------------------------------------
        # Names of the GeomInputs
        # -----------------------------------------------------------------------------

        run.GeomInput.Names = "box_input indi_input"

        # -----------------------------------------------------------------------------
        # Domain Geometry Input
        # -----------------------------------------------------------------------------

        run.GeomInput.box_input.InputType = "Box"
        run.GeomInput.box_input.GeomName = "domain"

        # run.Geom.domain.Patches = "x_lower x_upper y_lower y_upper z_lower z_upper"

        # -----------------------------------------------------------------------------
        # Domain
        # -----------------------------------------------------------------------------

        run.Domain.GeomName = "domain"

        # -----------------------------------------------------------------------------
        # Gravity
        # -----------------------------------------------------------------------------

        run.Gravity = 1.0
