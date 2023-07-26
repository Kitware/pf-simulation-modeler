from trame_server.utils.hot_reload import hot_reload
from trame.widgets import vuetify, html
from pf_simulation_modeler.widgets import pfsm as pf_widgets


@hot_reload
def simulation_type():
    with html.Div(classes="d-flex flex-column align-center justify-space-between"):
        pf_widgets.SimulationType(
            v_model=(
                "simTypeShortcuts",
                {
                    "wells": False,
                    "climate": True,
                    "contaminants": False,
                    "saturated": "Variably Saturated",
                },
            ),
        )
        with html.Div(classes="d-flex flex-column align-center mt-12"):
            html.P("What's the Simulation Name?", classes="text-h4 mb-2")
            html.P(
                "This will be used in the generated Python code.",
                classes="text-subtitle-2 grey--text",
            )
            vuetify.VTextField(
                label="Simulation Name",
                prepend_icon="mdi-atom",
                v_model=("sim_name",),
            )
