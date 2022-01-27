from trame import state
from trame.html import vuetify, Element, Div, Span, simput

from parflow import Run

from ..engine.files import FileDatabase, FileCategories

try:
    from paraview import simple

    VIZ_ENABLED = True
except:
    VIZ_ENABLED = False

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


@state.change("currentSoil")
def updateCurrentSoil(currentSoil, **kwargs):
    if not VIZ_ENABLED:
        return
    if soil_viz is None:
        return

    if currentSoil == "all":
        soil_viz.setSoilVisualizationMode("all")
    else:
        value = soil_viz.soilTypes[currentSoil]["value"]
        soil_viz.setSoilVisualizationMode("selection")
        soil_viz.activateSoil(value)

    html_view.update()


@state.change("domainView")
def on_view_change(domainView, indicatorFile, elevationFile, **kwargs):
    initialize_globals()
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
            if soil_viz is None:
                configFile = "LW_Test/LW_Test.pfidb"
                parflowConfig = Run.from_definition(configFile)
                parflowImage = SourceImage(parflowConfig, elevationFilePath)
                soil_viz = SoilVisualization(view, parflowImage, parflowConfig)

            soil_viz.indicatorFilename = indicatorFilePath
            soil_viz.parflowImage.elevationFilter.demFilename = elevationFilePath
            soil_viz.activate()

            state.update({"soils": ["all"] + list(soil_viz.soilTypes.keys())})


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

            with vuetify.VRow():
                with vuetify.VCol():
                    vuetify.VTextField(v_model=("LX", 1.0), label="lx", readonly=True)
                    vuetify.VTextField(v_model=("DX", 1.0), label="dx", readonly=True)
                    vuetify.VTextField(v_model=("NX", 1.0), label="nx", readonly=True)
                with vuetify.VCol():
                    vuetify.VTextField(v_model=("LY", 1.0), label="ly", readonly=True)
                    vuetify.VTextField(v_model=("DY", 1.0), label="dy", readonly=True)
                    vuetify.VTextField(v_model=("NY", 1.0), label="ny", readonly=True)
                with vuetify.VCol():
                    vuetify.VTextField(v_model=("LZ", 1.0), label="lz", readonly=True)
                    vuetify.VTextField(v_model=("DZ", 1.0), label="dz", readonly=True)
                    vuetify.VTextField(v_model=("NZ", 1.0), label="nz", readonly=True)

        with Div(classes="ma-6"):
            Span("Lorem Ipsum documentation for Indicator file")
            vuetify.VTextarea(
                v_if="indicatorFileDescription",
                value=("indicatorFileDescription", ""),
                readonly=True,
                style="font-family: monospace;",
            )


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


def create_domain_ui():
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
