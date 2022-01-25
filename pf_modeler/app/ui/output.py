from trame.html import vuetify, Element, Div, Span


def create_project_generation(
    validation_callback, validation_output, validation_check, run_variables
):
    with Div(
        classes="d-flex flex-column fill-height justify-space-around",
        v_if="currentView == 'Project Generation'",
    ):
        with Div(v_if=validation_check, classes="mx-6"):
            with vuetify.VCard(outlined=True, classes="pa-2 my-4"):
                vuetify.VCardTitle("Run variables")
                vuetify.VTextField(
                    v_model=(run_variables["BaseUnit"], 1.0),
                    label="TimingInfo.BaseUnit",
                )
                vuetify.VTextField(
                    v_model=(run_variables["DumpInterval"], 1.0),
                    label="TimingInfo.DumpInterval",
                )
                vuetify.VTextField(
                    v_model=(run_variables["StartCount"], 0),
                    label="TimingInfo.StartCount",
                )
                vuetify.VTextField(
                    v_model=(run_variables["StartTime"], 0.0),
                    label="TimingInfo.StartTime",
                )
                vuetify.VTextField(
                    v_model=(run_variables["StopTime"], 1000.0),
                    label="TimingInfo.StopTime",
                )
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

        with Div(v_if="projGenValidation.valid", classes="mx-6"):
            Span("Run Validated", classes="text-h5")
        with Div(classes="d-flex justify-end ma-6"):
            vuetify.VBtn(
                "Validate", click=validation_callback, color="primary", classes="mx-2"
            )
            vuetify.VBtn(
                "Generate", disabled=("!projGenValidation.valid"), color="primary"
            )
