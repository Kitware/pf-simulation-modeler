import os.path
from trame import state
from trame.html import vuetify, Element, simput

import yaml
from functools import partial

from ..engine.simput import KeyDatabase
from .. import engine

BASE_DIR = os.path.abspath(os.path.dirname(engine.__file__))

def on_bcp_change(id, topic, **kwargs):
    if topic != "update" and kwargs.get('property_name') != "Cycle":
        return

    pxm = KeyDatabase().pxm
    bcp = pxm.get(id)
    cycle_id = bcp["Cycle"]

    cycle = pxm.get(cycle_id)

    # Delete values defined for other cycles
    for value_id in state.BCPressureValueIds.get(id, []):
        pxm.delete(value_id)

    # Create new values for the new cycle
    state.BCPressureValueIds[id] = [
        pxm.create("BCPressureValue", SubCycle=sub_cycle_id).id for sub_cycle_id in cycle.own
    ]

    state.flush("BCPressureValueIds")


def initialize():
    patches = ["x_lower", "x_upper", "y_lower", "y_upper", "z_lower", "z_upper"]
    pxm = KeyDatabase().pxm
    bc_pressures = list(map(lambda patch: pxm.create('BCPressure', Patch=patch), patches))
    for bcp in bc_pressures:
        bcp.on(partial(on_bcp_change, bcp.id))

    bc_pressure_ids = list(map(lambda bcp: bcp.id, bc_pressures))

    state.update({
        "BCPressureIds": bc_pressure_ids,
        "BCPressureValueIds": {},
    })

@state.change("currentView")
def on_currentView_change(currentView, **kwargs):
    if currentView == 'Boundary Conditions':
        model_file = os.path.join(BASE_DIR, "model/boundary.yaml")
        with open(model_file)as f:
            model = yaml.load(f)

        pxm = KeyDatabase().pxm
        ui_manager = KeyDatabase().ui_manager

        cycles = list(map(lambda cycle: {"text": cycle['Name'], "value": cycle.id}, pxm.get_instances_of_type("Cycle")))

        model["BCPressure"]["Cycle"]["domains"] = [
            {"type": "LabelList", "values": cycles}
        ]

        sub_cycles = list(map(lambda cycle: {"text": cycle['Name'], "value": cycle.id}, pxm.get_instances_of_type("SubCycle")))

        model["BCPressureValue"]["SubCycle"]["domains"] = [
            {"type": "LabelList", "values": sub_cycles}
        ]

        model_content = yaml.dump(model)
        pxm.load_model(yaml_content=model_content)
        ui_manager.load_language(yaml_content=model_content)


def create_ui():
    Element("H1", "Boundary Conditions")

    with vuetify.VContainer(v_for=("(id, i) in BCPressureIds",), fluid=True):
        simput.SimputItem(itemId=("id",))
        with vuetify.VContainer(fluid=True, style="padding: 3rem;"):
            simput.SimputItem(v_for=("(valueId, vi) in BCPressureValueIds[id]",), itemId=("valueId",))
