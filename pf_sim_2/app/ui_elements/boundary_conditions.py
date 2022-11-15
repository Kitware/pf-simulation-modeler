from trame.widgets import vuetify, html, simput


class BoundaryConditions:
    def __init__(self, server):
        state, ctrl = server.state, server.controller
        self.server = server
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

    def page(self):
        html.H1("Boundary Conditions")
