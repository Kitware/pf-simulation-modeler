from trame_server.utils.hot_reload import hot_reload
from trame.widgets import vuetify, html, code


@hot_reload
def code_gen():
    html.H1("Generator")
    with vuetify.VContainer(fluid=True, classes="fill-height pa-0 justify-center"):
        code.Editor(
            style="width: 100%; height: 85vh;",
            value=("generated_code",),
            options=("editor_options", {}),
            language="python",
            theme=("editor_theme", "vs-dark"),
        )
