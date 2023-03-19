class SolverLogic:
    def __init__(self, state, ctrl):
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

        state.solver_outputs = [1, 2, 3]
        state.solver_id = self.pxm.create("Solver").id
        state.solver_nonlinear_id = self.pxm.create("SolverNonlinear").id
        state.solver_linear_id = self.pxm.create("SolverLinear").id


def initialize(server):
    state, ctrl = server.state, server.controller

    SolverLogic(state, ctrl)
