from trame.widgets import vuetify, html, simput
from .snippet import show_snippet


def solver(ctrl):
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
            simput.SimputItem(item_id=("solverId", None))
            html.H3("Nonlinear Parameters")
            simput.SimputItem(item_id=("solverNonlinearId", None))
            html.H3("Linear Parameters")
            simput.SimputItem(item_id=("solverLinearId", None))

    show_snippet(ctrl, "solver")
