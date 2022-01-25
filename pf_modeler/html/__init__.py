from trame.html import AbstractElement
from . import module

from trame.internal.app import get_app_instance

# Activate your Vue library
_app = get_app_instance()
_app.enable_module(module)


class FileDatabase(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("pf-file-database", children, **kwargs)
        self._attr_names += ["files", "db_update", "fileCategories", "error"]


class NavigationDropDown(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("pf-navigation-drop-down", children, **kwargs)
        self._attr_names += ["views"]


class SimulationType(AbstractElement):
    def __init__(self, children=None, **kwargs):
        super().__init__("pf-simulation-type", children, **kwargs)
        self._attr_names += ["shortcuts"]
