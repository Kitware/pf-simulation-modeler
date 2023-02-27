from trame_server.utils.hot_reload import hot_reload
from trame.widgets import vuetify, html, code


@hot_reload
def show_snippet(ctrl, snippet):
    with html.Div(
        style="position: fixed; top: 64px; right: 0; height: calc(100vh - 64px); display: flex; justify-content: flex-end; align-items: center;",
    ):
        with vuetify.VBtn(
            click=(ctrl.toggle_snippet, f"['{snippet}']"),
            style="min-width: 10px; min-height: 50px; padding: 2px; border-radius: 4px 0px 0px 4px; z-index: 3;",
        ):
            vuetify.VIcon(
                "mdi-chevron-left",
                style="height: 15px;",
                v_if="!display_snippet",
            )
            vuetify.VIcon(
                "mdi-chevron-right",
                style="height: 15px;",
                v_else="display_snippet",
            )

        with vuetify.VSlideXReverseTransition():
            with html.Div(
                v_if="display_snippet",
                style="width: 50vw; height: 100%; z-index: 3;",
            ):
                code.Editor(
                    style="width: 100%; height: 100%;",
                    value=("active_snippet",),
                    options=("editor_options", {}),
                    language="python",
                    theme=("editor_theme", "vs-dark"),
                )
