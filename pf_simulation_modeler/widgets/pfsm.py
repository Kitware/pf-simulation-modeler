from trame_client.widgets.core import AbstractElement
from .. import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


class FileDatabase(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "pf-file-database",
            **kwargs,
        )
        self._attr_names += ["files", "fileCategories", "error"]
        self._event_names += ["input"]


class SimulationType(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "pf-simulation-type",
            **kwargs,
        )
        self._event_names += ["input"]


class NavigationDropDown(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "pf-navigation-drop-down",
            **kwargs,
        )
        self._attr_names += ["views"]
        self._event_names += ["input"]
