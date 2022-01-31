r"""
Bind methods to the trame controller
"""

from pf_modeler.app.engine.simput import KeyDatabase
from trame import controller as ctrl
from . import engine


def bind_instances():
    ctrl.ui_set_key_database()


def bind_methods():
    ctrl.simput_save = KeyDatabase().save
    ctrl.validate_run = engine.validate_run


def on_start():
    engine.initialize()
    bind_instances()
    bind_methods()


def on_reload(reload_modules):
    """Method called when the module is reloaded

    reload_modules is a function that takes modules to reload

    We only need to reload the controller if the engine is reloaded.
    """
    # reload_modules(engine)
    bind_methods()
