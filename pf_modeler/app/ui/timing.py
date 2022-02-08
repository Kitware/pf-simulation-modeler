from trame import state
from trame.html import vuetify, Element, simput

from ..engine.simput import KeyDatabase

def update_cycle_list(*args, **kwargs):
    pxm = KeyDatabase().pxm
    cycleIds = []
    subCycleIds = {}
    for cycle in pxm.get_instances_of_type("Cycle"):
        cycleIds.append(cycle.id)
        subCycleIds[cycle.id] = []
        for subCycleId in cycle.own:
            subCycleIds[cycle.id].append(subCycleId)

    state.cycleIds = cycleIds
    state.subCycleIds = subCycleIds

def create_cycle(proxy_type, owner_id=None, **kwargs):
    pxm = KeyDatabase().pxm
    proxy = pxm.create(proxy_type, **kwargs)

    if owner_id is not None:
        owner = pxm.get(owner_id)
        owner._own.add(proxy.id)

    update_cycle_list()

    return proxy

def delete_cycle(id, proxy_type, owner_id=None):
    pxm = KeyDatabase().pxm

    if owner_id is not None:
        owner = pxm.get(owner_id)
        owner._own.remove(id)

    pxm.delete(id)

    update_cycle_list()

def initialize():
    state.update({
        "cycleIds": [],
        "subCycleIds": {},
    })

    cycle = create_cycle("Cycle", Name="constant", repeat=-1)
    create_cycle("SubCycle", cycle.id, Name="alltime", Length=1)

    cycle = create_cycle("Cycle", Name="rainrec", repeat=-1)
    create_cycle("SubCycle", cycle.id, Name="rain")
    create_cycle("SubCycle", cycle.id, Name="rec")

def create_ui():
    Element("H1", "Timing")
    simput.SimputItem(itemId=("timingId",))

    Element("H1", "Cycles")

    with vuetify.VContainer(v_for=("(cycleId, index) in cycleIds",), fluid=True):
        with vuetify.VContainer(style="display: flex;", fluid=True):
            simput.SimputItem(itemId=("cycleId",), style="flex-grow: 1;")
            with vuetify.VBtn(click=(delete_cycle, "[cycleId, 'Cycle']"), small=True, icon=True):
                vuetify.VIcon('mdi-delete')

        with vuetify.VContainer(fluid=True, style="padding: 2rem;"):
            with vuetify.VContainer(v_for=("(subId, subI) in subCycleIds[cycleId]",), fluid=True, style="display: flex;"):
                simput.SimputItem(itemId=("subId",), style="flex-grow: 1;")

                with vuetify.VBtn(click=(delete_cycle, "[subId, 'SubCycle', cycleId]"), small=True, icon=True):
                    vuetify.VIcon('mdi-delete')

            with vuetify.VBtn(click=(create_cycle, "['SubCycle', cycleId]")):
                vuetify.VIcon('mdi-plus')
                Element("span", "Add Sub Cycle")


    with vuetify.VBtn(click=(create_cycle, "['Cycle']")):
        vuetify.VIcon('mdi-plus')
        Element("span", "Add Cycle")
