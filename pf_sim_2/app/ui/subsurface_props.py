from trame_server.utils.hot_reload import hot_reload
from trame.widgets import simput, vuetify, html
from .snippet import show_snippet


@hot_reload
def subsurface_props(ctrl):
    with vuetify.VContainer(fluid=True, classes="pa-8"):
        html.H1("Regions")

        with html.Div(v_if="soil_ids.length === 0"):
            html.H2("No regions defined")
            html.P("Choose an indicator file to define regions.")

        with html.Div(v_if="soil_ids.length > 0"):
            simput.SimputItem(item_id=("domain_id",))
            simput.SimputItem(
                v_for=("(soil_id, index) in soil_ids",),
                item_id=("soil_id",),
            )
        show_snippet(ctrl, "subsurface_properties")
