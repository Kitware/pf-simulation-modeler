from trame_server.utils.hot_reload import hot_reload
from pf_simulation_modeler.widgets import pfsm as pf_widgets


@hot_reload
def file_db():
    pf_widgets.FileDatabase(
        files=("db_files",),
        fileCategories=("file_categories",),
        error=("upload_error",),
        v_model=("db_selected_file",),
    )
