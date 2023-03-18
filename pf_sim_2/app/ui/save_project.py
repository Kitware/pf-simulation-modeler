from trame_server.utils.hot_reload import hot_reload
from trame.widgets import vuetify, html


step_2_condition = "(!!indicator_filename && !!slope_x_filename && !!slope_y_filename && !!pressure_filename)"


@hot_reload
def save_project_button(ctrl, state):
    with vuetify.VDialog(v_model=("save_dialog",), persistent=False, max_width="600px"):
        with vuetify.Template(v_slot_activator="{ on, attrs }"):
            vuetify.VBtn(
                "Save",
                v_on="on",
                v_bind="attrs",
                color=("current_view === 'Code Generation' ? 'primary' : ''",),
                click="save_page = 1",
            )
        save_project(ctrl, state)

    progress_report()  # display success snackbar


@hot_reload
def save_project(ctrl, state):
    with vuetify.VCard(v_model="save_dialog"):
        with vuetify.VCardTitle():
            html.Span("Save Simulation")
        with vuetify.VStepper(v_model=("save_page",)):
            with vuetify.VStepperHeader(classes="justify-space-around"):
                with vuetify.VStepperStep(step="1", complete=("save_page > 1",)):
                    html.Span("Output Directory")
                with vuetify.VStepperStep(
                    step="2",
                    complete=("save_page > 2",),
                    rules=(f"[() => save_page < 2 || {step_2_condition}]",),
                ):
                    html.Span("Project Files")
                with vuetify.VStepperStep(step="3"):
                    html.Span("Project Code")

            with vuetify.VStepperItems():
                step_1()
                step_2()
                step_3(ctrl, state)


# ------------------------------------------------------------
# Save Project Steps
@hot_reload
def nav_buttons(backward, forward, disable_condition="false"):
    with html.Div(classes="d-flex justify-space-around flex-row mb-4"):
        vuetify.VBtn(backward[0], click=backward[1])
        vuetify.VBtn(
            forward[0], click=forward[1], color="primary", disabled=(disable_condition,)
        )


# Step 1: Output Directory
@hot_reload
def step_1():
    with vuetify.VStepperContent(step="1"):
        with html.Div(classes="mb-12", style="height: 130px"):
            html.H3("Project Export Directory")
            vuetify.VTextField(
                v_model=("sim_name",),
                label="Project Name",
                prepend_icon="mdi-atom",
                hide_details=True,
                classes="mb-4",
                style="max-width: max-content",
            )
            vuetify.VTextField(
                v_model=("output_directory",),
                label="Select Directory",
                prepend_icon="mdi-folder",
            )
        nav_buttons(("Cancel", "save_dialog = false"), ("Continue", "save_page = 2"))


# Step 2: Project Files
@hot_reload
def step_2():
    with vuetify.VStepperContent(step="2"):
        with html.Div(classes="mb-12", style="height: 290px"):
            html.H3("Export ParFlow Binary Files")
            with html.Ul(
                classes="d-flex flex-column align-center pa-0 ma-auto",
                style="width: 80%",
            ):
                # Indicator file
                with html.Li(
                    style="width: 100%",
                    classes="d-flex flex-row align-center justify-space-between mb-2",
                ):
                    html.P("Indicator", classes="mb-0 pa-2")
                    vuetify.VIcon("mdi-arrow-right")
                    select_file("indicator_filename", label="Indicator File")
                    no_file_selected(label="Indicator File")

                # Slope files
                with html.Li(
                    style="width: 100%",
                    classes="d-flex flex-row align-center justify-space-between mb-2",
                ):
                    html.P("Slope X", classes="mb-0 pa-2")
                    vuetify.VIcon("mdi-arrow-right")
                    select_file("slope_x_filename", label="Slope X File")
                    no_file_selected(label="Slope X File")

                with html.Li(
                    style="width: 100%",
                    classes="d-flex flex-row align-center justify-space-between mb-2",
                ):
                    html.P("Slope Y", classes="mb-0 pa-2")
                    vuetify.VIcon("mdi-arrow-right")
                    select_file("slope_y_filename", label="Slope Y File")
                    no_file_selected(label="Slope Y File")

                # Pressure file
                with html.Li(
                    style="width: 100%",
                    classes="d-flex flex-row align-center justify-space-between mb-2",
                ):
                    html.P("Pressure", classes="mb-0 pa-2")
                    vuetify.VIcon("mdi-arrow-right")
                    select_file("pressure_filename", label="Pressure File")
                    no_file_selected(label="Pressure File")

                # Elevation file (optional)
                with html.Li(
                    style="width: 100%",
                    classes="d-flex flex-row align-center justify-space-between",
                ):
                    html.P("Elevation", classes="mb-0 pa-2")
                    vuetify.VIcon("mdi-arrow-right")
                    select_file("elevation_filename", label="Elevation File (optional)")
                    no_file_selected(False, label="Elevation File (optional)")

        nav_buttons(
            ("Back", "save_page = 1"),
            ("Continue", "save_page = 3"),
            disable_condition=f"!{step_2_condition}",
        )


# Step 3: Project Code
@hot_reload
def step_3(ctrl, state):
    with vuetify.VStepperContent(step="3"):
        with html.Div(classes="mb-8", style="height: 100px"):
            html.H3("Export Python Code")
            with html.Div(
                classes="d-flex align-center justify-center",
                style="height: 80%",
            ):
                select_file(
                    "code_filename",
                    default=f"{state.sim_name}.py",
                    label="Project Code File",
                )
        nav_buttons(("Back", "save_page = 2"), ("Save", ctrl.save_project))


@hot_reload
def progress_report():
    with vuetify.VSnackbar(
        v_model="success_snackbar",
        timeout=(5000,),
        style="top: 0",
    ):
        html.Span(
            "Project Saved Successfully!",
        )

        with vuetify.Template(
            v_slot_action="{ attrs }",
        ):
            vuetify.VBtn(
                "Close",
                color="primary",
                v_bind="attrs",
                click="success_snackbar = false",
            )


# ------------------------------------------------------------
# File selection
@hot_reload
def select_file(filename, default=None, label=""):
    vuetify.VTextField(
        v_model=filename if default is None else (filename, default),
        v_if=filename,
        hide_details=True,
        label=label,
        prefix="/",
        prepend_icon="mdi-folder",
        classes="mb-0 pa-2",
        style="max-width: max-content",
    )


@hot_reload
def no_file_selected(error=True, label=""):
    vuetify.VTextField(
        value="Not Selected",
        v_else=True,
        hide_details=True,
        readonly=True,
        error=error,
        label=label,
        prefix="/",
        prepend_icon="mdi-folder",
        classes="mb-0 pa-2 font-italic v-input--is-disabled",
        style="max-width: max-content",
    )
