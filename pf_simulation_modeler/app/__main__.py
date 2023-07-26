from trame.app import get_server

from . import engine, ui


def main(
    server=None, output=None, input=None, datastore=None, sharedDir=None, **kwargs
):
    # Get or create server
    if server is None:
        server = get_server()

    if isinstance(server, str):
        server = get_server(server)

    if output is None:
        server.cli.add_argument(
            "-O", "--output", help="A working directory for the build", required=True
        )

    if input is None:
        server.cli.add_argument(
            "-I", "--input", help="An existing build directory to clone"
        )

    if datastore is None:
        server.cli.add_argument(
            "-D",
            "--datastore",
            help="A directory for tracking simulation input files",
            required=True,
        )

    if sharedDir is None:
        server.cli.add_argument(
            "-S",
            "--sharedir",
            help="A shared directory whose files can be selected from the client",
            required=True,
        )

    # Init application
    server.client_type = "vue2"
    engine.initialize(server)
    ui.UI(server)

    # Start server
    server.start(**kwargs)


if __name__ == "__main__":
    main()
