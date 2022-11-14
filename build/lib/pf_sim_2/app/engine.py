r"""
Define your classes and create the instances that you need to expose
"""
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------


class MyBusinessLogic:
    def __init__(self, server):
        self._server = server

        # initialize state + controller
        state, ctrl = server.state, server.controller
        # state.resolution = 6
        # ctrl.reset_resolution = self.reset_resolution
        # state.change("resolution")(self.on_resolution_change)

        state.update(
            {
                "dbFiles": {},
                "fileCategories": [
                    # {"value": cat.value, "text": file_category_label(cat)}
                    # for cat in FileCategories
                ],
                "uploadError": "",
                "dbSelectedFile": None,

                "currentView": "File Database",
                "views": [
                    "File Database",
                    "Simulation Type",
                    "Domain",
                    "Timing",
                    "Boundary Conditions",
                    "Subsurface Properties",
                    "Solver",
                    "Project Generation",
                ],
                #
                # **validated_args,
                # "dbFiles": entries,
                # "dbSelectedFile": None if not entries else list(entries.values())[0],
            }
        )

        ctrl.uploadFile = self.uploadFile
        ctrl.uploadLocalFile = self.uploadLocalFile
        ctrl.updateFiles = self.updateFiles

    # def reset_resolution(self):
    #     self._server.state.resolution = 6

    # def on_resolution_change(self, resolution, **kwargs):
    #     logger.info(f">>> ENGINE(a): Slider updating resolution to {resolution}")

    def uploadFile(self, kwargs):
        logger.info(f">>> uploadLocalFile: {kwargs}")

    def uploadLocalFile(self, entryId, fileMeta):
        logger.info(f">>> uploadLocalFile: {entryId} {fileMeta}")

    def updateFiles(self, update, entryId=None):
        logger.info(f">>> updateFiles: {update} {entryId}")


# ---------------------------------------------------------
# Server binding
# ---------------------------------------------------------


def initialize(server):
    state, ctrl = server.state, server.controller

    # @state.change("resolution")
    # def resolution_changed(resolution, **kwargs):
    #     logger.info(f">>> ENGINE(b): Slider updating resolution to {resolution}")

    def protocols_ready(**initial_state):
        logger.info(f">>> ENGINE(b): Server is ready {initial_state}")

    # Add args to parser
    # parser = get_cli_parser()
    # args = register_arguments(parser)

    # Add validated args to initial state
    # validator = ArgumentsValidator(args)
    # if not validator.valid:
    #     parser.print_help(sys.stderr)
    # validated_args = validator.args

    # Init singletons
    # file_database = FileDatabase()
    # file_database.datastore = validated_args.get("datastore")
    # entries = file_database.getEntries()


    # file_changes()

    ctrl.on_server_ready.add(protocols_ready)

    engine = MyBusinessLogic(server)
    return engine
