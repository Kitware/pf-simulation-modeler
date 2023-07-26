from trame_server.utils.hot_reload import hot_reload
from trame.widgets import vuetify, html


@hot_reload
def pressure(ctrl):
    with vuetify.VContainer(classes="pa-2 pt-4"):
        html.H1("Pressure")
        html.P("Select a pressure file and patch to apply a pressure boundary patch.")

        with html.Div(classes="d-flex flex-column justify-center align-start"):
            vuetify.VSelect(
                v_model=("pressure_file",),
                placeholder="Select Pressure File",
                items=(
                    "Object.values(db_files).filter(file => file.category === 'Pressure')",
                ),
                item_text="name",
                item_value="id",
            )

            vuetify.VSelect(
                v_model=("pressure_patch",),
                placeholder="Select Patch",
                items=("bc_patch_names",),
                item_text="name",
                item_value="id",
            )
