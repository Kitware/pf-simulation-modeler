from trame import state
from trame.html import vuetify, Element, Div, Span, simput

from parflow import Run
from parflowio.pyParflowio import PFData

from ..engine.files import FileDatabase, FileCategories
from ..engine.simput import KeyDatabase

try:
    from paraview import simple

    VIZ_ENABLED = True
except:
    VIZ_ENABLED = False



def initialize():
    state.update(
        {
            "domainView": "grid",
            "soils": [],
            "currentSoil": "all",
            "indicatorFile": None,
            "slopeXFile": None,
            "slopeYFile": None,
            "elevationFile": None,
        }
    )

if VIZ_ENABLED:
    from trame.html import paraview
    from pf_modeler.app.engine.visualizations.image import SourceImage
    from pf_modeler.app.engine.visualizations.soil import SoilVisualization

    view = simple.GetRenderView()
    html_view = paraview.VtkRemoteView(view)
    soil_viz = None

@state.change("indicatorFile")
def updateComputationalGrid(indicatorFile, **kwargs):
    file_database = FileDatabase()
    key_database = KeyDatabase()

    entry = file_database.getEntry(indicatorFile)
    state.indicatorFileDescription = entry.get("description")

    filename = file_database.getEntryPath(indicatorFile)
    try:
        handle = PFData(filename)
    except:
        print(f"Could not find pfb: {filename}")
        raise
    handle.loadHeader()

    change_set = [
        {"id": state.gridId, "name": "Origin", "value": [handle.getX(), handle.getY(), handle.getZ()]},
        {"id": state.gridId, "name": "Spacing", "value": [handle.getDX(), handle.getDY(), handle.getDZ()]},
        {"id": state.gridId, "name": "Size", "value": [handle.getNX(), handle.getNY(), handle.getNZ()]},
    ]

    for soilId in state.soilIds:
        key_database.pxm.delete(soilId)

    state.soilIds = []

    key_database.pxm.update(change_set)

    handle.loadData()

    data = handle.viewDataArray()

    unique_values = set()

    for val in data.flat:
        unique_values.add(round(val))

    handle.close()

    soil_ids = []
    for val in unique_values:
        soil = key_database.pxm.create('Soil', **{"Key": f"s{val}", "Value": val})
        soil_ids.append(soil.id)

    state.soilIds = soil_ids

@state.change("currentSoil")
def updateCurrentSoil(currentSoil, **kwargs):
    if not VIZ_ENABLED:
        return
    if soil_viz is None:
        return

    if currentSoil == "all":
        soil_viz.setSoilVisualizationMode("all")
    else:
        value = currentSoil
        soil_viz.setSoilVisualizationMode("selection")
        soil_viz.activateSoil(value)

    html_view.update()


@state.change("domainView")
def on_view_change(domainView, indicatorFile, elevationFile, **kwargs):
    if not VIZ_ENABLED:
        return

    global soil_viz

    if domainView == "grid":
        if soil_viz is not None:
            pass

    elif domainView == "viz":
        if indicatorFile is None or elevationFile is None:
            state.domainView = "grid"
            return

        indicatorFilePath = FileDatabase().getEntryPath(indicatorFile)
        elevationFilePath = FileDatabase().getEntryPath(elevationFile)

        if indicatorFilePath is not None and elevationFilePath is not None:
            pxm = KeyDatabase().pxm
            grid = pxm.get(state.gridId)
            if soil_viz is None:
                parflowImage = SourceImage(grid, elevationFilePath)
                soil_viz = SoilVisualization(view, parflowImage)

            soil_viz.indicatorFilename = indicatorFilePath
            soil_viz.parflowImage.elevationFilter.demFilename = elevationFilePath
            soil_viz.activate()

            def soilOptionMapper(id):
                soil = pxm.get(id)
                return {"text": soil.Key, "value": soil.Value}

            soilOptions = list(map(soilOptionMapper, state.soilIds))

            state.update({"soils": [{"text": "All", "value": "all"}] + soilOptions})


def domain_viz(parent):
    if not VIZ_ENABLED:
        return

    vuetify.VSelect(
        label="Current Soil",
        v_model=("currentSoil",),
        items=("soils",),
    )

    parent.add_child(html_view)


def domain_parameters():
    Element("H1", "Indicator")
    with vuetify.VRow(classes="ma-6 justify-space-between"):
        with Div():
            vuetify.VSelect(
                v_model=("indicatorFile", None),
                placeholder="Select an indicator file",
                items=(
                    f"Object.values(dbFiles).filter(function(file){{return file.category === '{FileCategories.Indicator}'}})",
                ),
                item_text="name",
                item_value="id",
            )

            Element("H3", "Grid")

            simput.SimputItem(itemId=("gridId",))

def terrain_parameters():
    Element("H1", "Terrain")
    with vuetify.VRow(classes="ma-6 justify-space-between"):
        with vuetify.VCol():
            vuetify.VSelect(
                v_model=("slopeXFile",),
                placeholder="Select a Slope X file",
                items=(
                    f"Object.values(dbFiles).filter(function(file){{return file.category === '{FileCategories.Slope}'}})",
                ),
                item_text="name",
                item_value="id",
            )
        with vuetify.VCol():
            vuetify.VSelect(
                v_model=("slopeYFile",),
                placeholder="Select a Slope Y file",
                items=(
                    f"Object.values(dbFiles).filter(function(file){{return file.category === '{FileCategories.Slope}'}})",
                ),
                item_text="name",
                item_value="id",
            )
        with vuetify.VCol():
            vuetify.VSelect(
                v_model=("elevationFile",),
                placeholder="Select an elevation file",
                items=(
                    f"Object.values(dbFiles).filter(function(file){{return file.category === '{FileCategories.Elevation}'}})",
                ),
                item_text="name",
                item_value="id",
            )


def create_ui():
    with Div(classes="d-flex flex-column fill-height", v_if="currentView == 'Domain'"):
        with vuetify.VToolbar(
            flat=True, classes="fill-width align-center grey lighten-2 flex-grow-0"
        ):
            vuetify.VToolbarTitle("Domain Parameters")
            vuetify.VSpacer()
            with vuetify.VBtnToggle(
                rounded=True, mandatory=True, v_model=("domainView",)
            ):
                with vuetify.VBtn(small=True, value="grid"):
                    vuetify.VIcon("mdi-format-align-left", small=True, classes="mr-1")
                    Span("Parameters")
                with vuetify.VBtn(
                    small=True,
                    value="viz",
                    disabled=("!indicatorFile || !elevationFile",),
                ):
                    vuetify.VIcon("mdi-eye", small=True, classes="mr-1")
                    Span("Preview")
        with Div(
            v_if="domainView=='grid'",
            classes="fill-height fill-width flex-grow-1 ma-6",
        ):
            domain_parameters()
            terrain_parameters()

        with vuetify.VContainer(
            v_if="domainView=='viz'",
            fluid=True,
            classes="pa-0 fill-height",
        ) as parent:
            domain_viz(parent)
