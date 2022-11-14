from trame.widgets import vuetify, html, simput


class Domain:
    def __init__(self, server, pxm):
        self.state, self.ctrl = server.state, server.controller

        self.state.update(
            {
                "domainView": "grid",
                "soils": [],
                "currentSoil": "all",
                "indicatorFile": None,
                "slopeXFile": None,
                "slopeYFile": None,
                "elevationFile": None,

                'gridId': pxm.create("ComputationalGrid").id,
            }
        )

        self.pxm = pxm


        change_set = [
            {"id": self.state.gridId, "name": "Origin", "value": [0, 0, 0]}, # TODO: add the original handler code
            {"id": self.state.gridId, "name": "Spacing", "value": [0, 0, 0]}, # TODO: see above
            {"id": self.state.gridId, "name": "Size", "value": [0, 0, 0]}, # TODO: see above
        ]
        self.pxm.update(change_set)

    def domain_parameters(self):
        html.H1("Indicator")
        with vuetify.VRow(classes="ma-6 justify-space-between"):
            with html.Div():
                vuetify.VSelect(
                    v_model=("indicatorFile", None),
                    placeholder="Select an indicator file",
                    items=(
                        # f"Object.values(dbFiles).filter(function(file){{return file.category === '{FileCategories.Indicator}'}})",
                    ),
                    item_text="name",
                    item_value="id",
                )

                html.H3("Grid")
                simput.SimputItem(itemId=("gridId",))

    def page(self):
        with html.Div(classes="d-flex flex-column fill-height", v_if="currentView == 'Domain'"):
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
            with html.Div(
                v_if="domainView=='grid'",
                classes="fill-height fill-width flex-grow-1 ma-6",
            ):
                self.domain_parameters()
            #     terrain_parameters()

            # with vuetify.VContainer(
            #     v_if="domainView=='viz'",
            #     fluid=True,
            #     classes="pa-0 fill-height",
            # ) as parent:
            #     domain_viz(parent)