from trame_server.utils.hot_reload import hot_reload
from trame.widgets import vuetify, html, simput
from .snippet import show_snippet


@hot_reload
def solver(ctrl):
    with vuetify.VContainer(fluid=True, classes="pa-4"):
        html.H1("Solver")

        with vuetify.VContainer(fluid=True):
            html.H2("Outputs")
            with vuetify.VChipGroup(v_model=("solver_outputs",), multiple=True):
                with vuetify.VChip(outlined=True, filter=True):
                    html.H4("Subsurface Data")

                with vuetify.VChip(outlined=True, filter=True):
                    html.H4("Pressure")

                with vuetify.VChip(outlined=True, filter=True):
                    html.H4("Saturation")

                with vuetify.VChip(outlined=True, filter=True):
                    html.H4("Mask")

        with vuetify.VContainer(fluid=True):
            html.H2("Parameters")
            with vuetify.VContainer(fluid=True):
                html.H3("General Parameters")
                simput.SimputItem(item_id=("solver_id", None))
                html.H3("Nonlinear Parameters")
                simput.SimputItem(item_id=("solver_nonlinear_id", None))
                html.H3("Linear Parameters")
                simput.SimputItem(item_id=("solver_linear_id", None))

        show_snippet(ctrl, "solver")
