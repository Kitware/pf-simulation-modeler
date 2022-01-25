import os.path
import yaml

from trame import state, controller as ctrl

from simput.core import ProxyManager, UIManager, ProxyDomainManager
from simput.ui.web import VuetifyResolver
from simput.domains import register_domains
from simput.values import register_values

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Simput registrations
register_domains()
register_values()


class KeyDatabase:
    def __init__(self, work_dir):
        self._work_dir = work_dir

        # Load Simput models and layouts
        self._pxm = ProxyManager()
        ui_resolver = VuetifyResolver()
        self._ui_manager = UIManager(self._pxm, ui_resolver)
        self._pdm = ProxyDomainManager()
        self._pxm.add_life_cycle_listener(self._pdm)
        self._pxm.load_model(yaml_file=os.path.join(BASE_DIR, "model/model.yaml"))
        self._ui_manager.load_ui(xml_file=os.path.join(BASE_DIR, "model/layout.xml"))
        self._ui_manager.load_language(
            yaml_file=os.path.join(BASE_DIR, "model/model.yaml")
        )
        self._ui_manager.load_language(
            yaml_file=os.path.join(BASE_DIR, "model/lang/en.yaml")
        )

        # Initialize model_types for parflow keys
        settings_path = os.path.join(work_dir, "pf_settings.yaml")
        with open(settings_path, "r") as settings_file:
            settings = yaml.safe_load(settings_file)

        # Either load from previous save or instantiate models
        model_types = self._pxm.types()
        if settings.get("save"):
            self._pxm.load(file_content=settings.get("save"))
            for model_type in model_types:
                setattr(
                    self, model_type, self._pxm.get_instances_of_type(model_type)[0]
                )

        else:
            for model_type in model_types:
                setattr(self, model_type, self._pxm.create(model_type))

    @property
    def pxm(self):
        return self._pxm

    @property
    def pdm(self):
        return self._pdm

    @property
    def ui_manager(self):
        return self._ui_manager

    def save(self):
        settings_path = os.path.join(self._work_dir, "pf_settings.yaml")
        with open(settings_path, "r+") as settings_file:
            settings = yaml.safe_load(settings_file)
            settings["save"] = self._pxm.save()
            yaml.dump(settings, settings_file)
