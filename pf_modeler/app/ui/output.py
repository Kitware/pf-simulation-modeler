from trame.html import vuetify, Element, Div, Span


def create_project_generation(
    validation_callback, validation_output, validation_check
):
    with Div(
        classes="d-flex flex-column fill-height justify-space-around",
        v_if="currentView == 'Project Generation'",
    ):
        with Div(classes="mx-6"):
            with vuetify.VCard(dark=True, outlined=True, classes="pa-2 my-4"):
                vuetify.VCardTitle("Validation console output")
                vuetify.VDivider()
                vuetify.VTextarea(
                    value=(validation_output,),
                    dark=True,
                    readonly=True,
                    style="font-family: monospace;",
                )
            vuetify.VSpacer()

        with Div(v_if=(validation_check, ), classes="mx-6"):
            Span("Run Validated", classes="text-h5")
        with Div(classes="d-flex justify-end ma-6"):
            vuetify.VBtn(
                "Validate", click=validation_callback, color="primary", classes="mx-2"
            )
            vuetify.VBtn(
                "Generate", disabled=(f"!{validation_check}", ), color="primary"
            )
