from trame_simput.core.proxy import Proxy


def get_prop(proxy, name, default=None):
    value = proxy.get_property(name, default)
    if value is None:
        return default
    return value


class SolverSnippet:
    def __init__(self, state, ctrl):
        self.state, self.ctrl = state, ctrl
        self.pxm = self.ctrl.get_pxm()

        self.output_code = ""
        self.general_code = ""
        self.nonlinear_code = ""
        self.linear_code = ""

    def set_output(self):
        outputs = self.state.solver_outputs
        code = "# Outputs\n"
        code += f"LW_Test.Solver.PrintSubsurfData = {0 in outputs}\n"
        code += f"LW_Test.Solver.PrintPressure = {1 in outputs}\n"
        code += f"LW_Test.Solver.PrintSaturation = {2 in outputs}\n"
        code += f"LW_Test.Solver.PrintMask = {3 in outputs}\n"
        self.output_code = code

    def set_general(self):
        proxy: Proxy = self.pxm.get(self.state.solver_id)
        if not proxy:
            return

        # TODO: Make default values more reasonable
        max_iter = get_prop(proxy, "MaxIter", 25000)
        drop = get_prop(proxy, "Drop", 1e-20)
        abs_tol = get_prop(proxy, "AbsTol", 1e-8)
        max_convergence_failures = get_prop(proxy, "MaxConvergenceFailures", 8)
        terrain_following_grid = get_prop(proxy, "TerrainFollowingGrid", True)

        code = "# General Solver parameters\n"
        code += f"LW_Test.Solver.MaxIter = {max_iter}\n"
        code += f"LW_Test.Solver.Drop = {drop}\n"
        code += f"LW_Test.Solver.AbsTol = {abs_tol}\n"
        code += f"LW_Test.Solver.MaxConvergenceFailures = {max_convergence_failures}\n"
        code += f"LW_Test.Solver.TerrainFollowingGrid = {terrain_following_grid}\n"
        self.general_code = code

    def set_nonlinear(self):
        proxy: Proxy = self.pxm.get(self.state.solver_nonlinear_id)
        if not proxy:
            return

        max_iter = get_prop(proxy, "MaxIter", 80)
        residual_tol = get_prop(proxy, "ResidualTol", 1e-6)
        eta_value = get_prop(proxy, "EtaValue", 1e-3)
        derivative_epsilon = get_prop(proxy, "DerivativeEpsilon", 1e-16)
        step_tol = get_prop(proxy, "StepTol", 1e-30)
        globalization = get_prop(proxy, "Globalization", "LineSearch")
        variable_dz = get_prop(proxy, "VariableDz", False)

        code = "# Nonlinear Solver parameters\n"
        code += f"LW_Test.Solver.Nonlinear.MaxIter = {max_iter}\n"
        code += f"LW_Test.Solver.Nonlinear.ResidualTol = {residual_tol}\n"
        code += f"LW_Test.Solver.Nonlinear.EtaValue = {eta_value}\n"
        code += f"LW_Test.Solver.Nonlinear.DerivativeEpsilon = {derivative_epsilon}\n"
        code += f"LW_Test.Solver.Nonlinear.StepTol = {step_tol}\n"
        code += f"LW_Test.Solver.Nonlinear.Globalization = '{globalization}'\n"
        code += f"LW_Test.Solver.Nonlinear.VariableDz = {variable_dz}\n"
        self.nonlinear_code = code

    def set_linear(self):
        proxy: Proxy = self.pxm.get(self.state.solver_linear_id)
        if not proxy:
            return

        krylov_dimension = get_prop(proxy, "KrylovDimension", 70)
        max_restarts = get_prop(proxy, "MaxRestarts", 2)

        code = "# Linear Solver parameters\n"
        code += f"LW_Test.Solver.Linear.KrylovDimension = {krylov_dimension}\n"
        code += f"LW_Test.Solver.Linear.MaxRestarts = {max_restarts}\n"
        self.linear_code = code

    @property
    def header(self):
        header = "# ------------------------------\n"
        header += "# Solver\n"
        header += "# ------------------------------"
        return header

    @property
    def snippet(self):
        self.set_output()
        self.set_general()
        self.set_nonlinear()
        self.set_linear()
        return "\n".join(
            [
                self.header,
                self.output_code,
                self.general_code,
                self.nonlinear_code,
                self.linear_code,
            ]
        )
