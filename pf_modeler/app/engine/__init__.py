r"""
Define your classes and create the instances that you need to expose
"""
import sys

from .cli import register_arguments, ArgumentsValidator
from .files import FileDatabase, file_changes, FileCategories, file_category_label
from .simput import KeyDatabase
from .output import validate_run

from trame import state, get_cli_parser

__all__ = [
    "initialize",
    "validate_run",
]

# ---------------------------------------------------------
# CLI handling
# ---------------------------------------------------------


def initialize():
    """Initialize application at startup"""
    # Add args to parser
    parser = get_cli_parser()
    args = register_arguments(parser)

    # Add validated args to initial state
    validator = ArgumentsValidator(args)
    if not validator.valid:
        parser.print_help(sys.stderr)
    validated_args = validator.args

    # Init singletons
    file_database = FileDatabase()
    file_database.datastore = validated_args.get("datastore")
    entries = file_database.getEntries()

    key_database = KeyDatabase()

    # Update state with some initial values
    state.update(
        {
            # UI
            "currentView": "File Database",
            "views": [
                "File Database",
                "Simulation Type",
                "Domain",
                "Boundary Conditions",
                "Subsurface Properties",
                "Solver",
                "Project Generation",
            ],
            "fileCategories": [
                {"value": cat.value, "text": file_category_label(cat)}
                for cat in FileCategories
            ],
            "uploadError": "",
            "dbFiles": {},
            "dbSelectedFile": None,
            "dbFileExchange": None,
            "solverSearchIndex": {},
            "solverSearchIds": [],
            "projGenValidation": {
                "valid": False,
                "output": "Parflow run did not validate.\nSolver.TimeStep must be type Int, found 3.14159",
            },
            # file database
            **validated_args,
            "dbFiles": entries,
            "dbSelectedFile": None if not entries else list(entries.values())[0],
            # Simput key ids
            # Domain
            "gridId": key_database.pxm.create("ComputationalGrid").id,
            "soilIds": [],
        }
    )

    # Finish engine initialization
    file_changes()
