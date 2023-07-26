from trame_server.utils.hot_reload import hot_reload
from trame.widgets import vuetify, html, simput
from .snippet import show_snippet


@hot_reload
def domain_parameters():
    html.H1("Indicator")
    with vuetify.VRow(classes="ma-6 justify-space-between"):
        with html.Div():
            vuetify.VSelect(
                v_model=("indicator_file", None),
                placeholder="Select an indicator file",
                items=(
                    "Object.values(db_files).filter(f => f.category.toLowerCase() === 'indicator')",
                ),
                item_text="name",
                item_value="id",
            )

            html.H3("Grid")
            simput.SimputItem(item_id=("grid_id", None))


@hot_reload
def terrain_parameters():
    html.H1("Terrain")
    with html.Div(classes="ma-6"):
        with vuetify.VRow(classes="mx-6"):
            vuetify.VSelect(
                v_model=("slope_x_file",),
                placeholder="Select a Slope X file",
                items=(
                    "Object.values(db_files).filter(f => f.category.toLowerCase() === 'slope')",
                ),
                item_text="name",
                item_value="id",
            )
        with vuetify.VRow(classes="mx-6"):
            vuetify.VSelect(
                v_model=("slope_y_file",),
                placeholder="Select a Slope Y file",
                items=(
                    "Object.values(db_files).filter(f => f.category.toLowerCase() === 'slope')",
                ),
                item_text="name",
                item_value="id",
            )
        with vuetify.VRow(classes="mx-6"):
            vuetify.VSelect(
                v_model=("elevation_file",),
                placeholder="Select an elevation file",
                items=(
                    "Object.values(db_files).filter(f => f.category.toLowerCase() === 'elevation')",
                ),
                item_text="name",
                item_value="id",
            )


@hot_reload
def bounds():
    html.H1("Bounds")
    html.P("Box domain")
    vuetify.VTextField(
        label="Domain Name",
        v_model=("domain_geom_name",),
        hide_details=True,
        classes="pb-3",
    )
    bounds = {
        "X Bound": "x_bound",
        "Y Bound": "y_bound",
        "Z Bound": "z_bound",
    }
    with html.Div(classes="d-flex flex-row"):
        for name, bound in bounds.items():
            with html.Div(classes="px-2 d-flex flex-md-column"):
                vuetify.VTextField(
                    v_model=(f"{bound}[0]",),
                    label=name,
                    readonly=True,
                    hide_details=True,
                )
                vuetify.VTextField(
                    v_model=(f"{bound}[1]",),
                    readonly=True,
                    hide_details=True,
                    classes="ma-0 pa-0",
                )

    html.H1("Patches", classes="pt-12")
    html.P("Define patch names")
    simput.SimputItem(item_id=("patches_id",))


@hot_reload
def domain(ctrl):
    with html.Div(classes="d-flex flex-column fill-height"):
        with vuetify.VToolbar(
            flat=True, classes="fill-width align-center grey lighten-2 flex-grow-0"
        ):
            vuetify.VToolbarTitle("Domain Parameters")
            vuetify.VSpacer()
            with vuetify.VBtnToggle(
                rounded=True, mandatory=True, v_model=("domain_view",)
            ):
                with vuetify.VBtn(small=True, value="grid"):
                    vuetify.VIcon("mdi-format-align-left", small=True, classes="mr-1")
                    html.Span("Parameters")
                with vuetify.VBtn(
                    small=True,
                    value="viz",
                    disabled=("!indicator_file || !elevation_file",),
                ):
                    vuetify.VIcon("mdi-eye", small=True, classes="mr-1")
                    html.Span("Preview")

        # Page content
        with vuetify.VContainer(
            v_if="domain_view=='grid'",
            classes="fill-height fill-width pa-0",
        ):
            with vuetify.VCol(classes="fill-height"):
                domain_parameters()
                terrain_parameters()
            with vuetify.VCol(classes="fill-height"):
                bounds()

        show_snippet(ctrl, "domain")

        with vuetify.VContainer(
            v_if="domain_view=='viz'",
            fluid=True,
            classes="pa-0 fill-height",
        ):
            html.P("TODO: add the visualization here")
        #     domain_viz(parent)
