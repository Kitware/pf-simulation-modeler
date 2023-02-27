from trame_server.utils.hot_reload import hot_reload
from trame.widgets import simput, html
from .snippet import show_snippet


@hot_reload
def subsurface_props(ctrl):
    html.H1("Regions")

    with html.Div(v_if="soil_ids.length === 0"):
        html.H2("No regions defined")
        html.P("Choose an indicator file to define regions.")

    with html.Div(v_if="soil_ids.length > 0"):
        simput.SimputItem(item_id=("domain_id", None))
        simput.SimputItem(
            v_for=("(soil_id, index) in soil_ids",),
            item_id=("soil_id", None),
        )
    show_snippet(ctrl, "subsurface_properties")
