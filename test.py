import openmdao.api as om
import numpy as np

# Custom component for the objective
class Paraboloid(om.ExplicitComponent):
    """
    Evaluates f(x,y) = (x-4)^2 + xy + (y+3)^2 - 3.
    """

    def setup(self):
        self.add_input('x', val=0.0)
        self.add_input('y', val=0.0)
        self.add_output('f_xy', val=0.0)

        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs):
        x = inputs['x']
        y = inputs['y']
        outputs['f_xy'] = (x - 4.0)**2 + x * y + (y + 3.0)**2 - 3.0

# Constraint component: g1(x,y) = x^2 + y - 1 >= 0, g2(x,y) = 8 - x^2 - y >= 0
class Constraints(om.ExplicitComponent):

    def setup(self):
        self.add_input('x', val=0.0)
        self.add_input('y', val=0.0)

        self.add_output('g1', val=0.0)
        self.add_output('g2', val=0.0)

        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs):
        x = inputs['x']
        y = inputs['y']

        outputs['g1'] = x**2 + y - 1.0       # must be >= 0
        outputs['g2'] = 8.0 - x**2 - y       # must be >= 0

if __name__ == "__main__":
    prob = om.Problem()

    model = prob.model
    model.add_subsystem('parab_comp', Paraboloid(), promotes=['x', 'y', 'f_xy'])
    model.add_subsystem('constraints', Constraints(), promotes=['x', 'y', 'g1', 'g2'])

    # Objective
    model.add_objective('f_xy')

    # Design variables
    model.add_design_var('x', lower=-50, upper=50)
    model.add_design_var('y', lower=-50, upper=50)

    # Constraints
    model.add_constraint('g1', lower=0.0)
    model.add_constraint('g2', lower=0.0)

    # Driver
    prob.driver = om.ScipyOptimizeDriver()
    prob.driver.options['optimizer'] = 'SLSQP'
    prob.driver.options['tol'] = 1e-9

    prob.setup()

    # Initial guess
    prob.set_val('x', 0.0)
    prob.set_val('y', 0.0)

    prob.run_driver()

    x_opt = prob.get_val('x')[0]
    y_opt = prob.get_val('y')[0]
    f_opt = prob.get_val('f_xy')[0]

    print(f"Optimal x: {x_opt:.3f}")
    print(f"Optimal y: {y_opt:.3f}")
    print(f"Minimum f(x,y): {f_opt:.3f}")
