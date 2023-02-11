from trame.widgets import vuetify, html, simput
from .snippet import show_snippet


def domain_parameters():
    html.H1("Indicator")
    with vuetify.VRow(classes="ma-6 justify-space-between"):
        with html.Div():
            vuetify.VSelect(
                v_model=("indicatorFile", None),
                placeholder="Select an indicator file",
                items=(
                    "Object.values(dbFiles).filter(function(file){return file.category === 'Indicator'})",
                ),
                item_text="name",
                item_value="id",
            )

            html.H3("Grid")
            simput.SimputItem(item_id=("gridId", None))


def terrain_parameters():
    html.H1("Terrain")
    with html.Div(classes="ma-6"):
        with vuetify.VRow(classes="mx-6"):
            vuetify.VSelect(
                v_model=("slopeXFile",),
                placeholder="Select a Slope X file",
                items=(
                    "Object.values(dbFiles).filter(function(file){return file.category === 'Slope'})",
                ),
                item_text="name",
                item_value="id",
            )
        with vuetify.VRow(classes="mx-6"):
            vuetify.VSelect(
                v_model=("slopeYFile",),
                placeholder="Select a Slope Y file",
                items=(
                    "Object.values(dbFiles).filter(function(file){return file.category === 'Slope'})",
                ),
                item_text="name",
                item_value="id",
            )
        with vuetify.VRow(classes="mx-6"):
            vuetify.VSelect(
                v_model=("elevationFile",),
                placeholder="Select an elevation file",
                items=(
                    "Object.values(dbFiles).filter(function(file){return file.category === 'Elevation'})",
                ),
                item_text="name",
                item_value="id",
            )


def bounds():
    html.H1("Bounds")
    html.P("Box domain")
    simput.SimputItem(item_id=("bounds_id",))

    html.H1("Patches", classes="pt-12")
    html.P("Define patch names")
    simput.SimputItem(item_id=("patches_id",))


def domain(ctrl):
    with html.Div(classes="d-flex flex-column fill-height"):
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
                    html.Span("Parameters")
                with vuetify.VBtn(
                    small=True,
                    value="viz",
                    disabled=("!indicatorFile || !elevationFile",),
                ):
                    vuetify.VIcon("mdi-eye", small=True, classes="mr-1")
                    html.Span("Preview")

        with vuetify.VContainer(
            v_if="domainView=='grid'",
            classes="fill-height fill-width pa-0",
        ):
            with vuetify.VCol(classes="fill-height"):
                domain_parameters()
                terrain_parameters()
            with vuetify.VCol(classes="fill-height"):
                bounds()

        show_snippet(ctrl, "domain")

        with vuetify.VContainer(
            v_if="domainView=='viz'",
            fluid=True,
            classes="pa-0 fill-height",
        ) as parent:
            html.P("TODO: add the visualization here")
        #     domain_viz(parent)
