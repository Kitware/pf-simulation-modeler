class SolverLogic:
    def __init__(self, state, ctrl):
        self.state = state
        self.ctrl = ctrl
        self.pxm = ctrl.get_pxm()

        state.update(
            {
                "solver_outputs": [1, 2, 3],
            }
        )
        state.solverId = self.pxm.create("Solver").id
        state.solverNonlinearId = self.pxm.create("SolverNonlinear").id
        state.solverLinearId = self.pxm.create("SolverLinear").id


def initialize(server):
    state, ctrl = server.state, server.controller

    SolverLogic(state, ctrl)
