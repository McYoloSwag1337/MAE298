import openmdao.api as om

class Paraboloid(om.ExplicitComponent):
    """
    Evaluates the equation f(x,y) = (x-4)^2 + xy + (y+3)^2 - 3.
    """

    def setup(self):
        self.add_input('x', val=0.0)
        self.add_input('y', val=0.0)

        self.add_output('f_xy', val=0.0)

    def setup_partials(self):
        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs):
       
        x = inputs['x']
        y = inputs['y']

        outputs['f_xy'] = (x - 4.0)**2 + x * y + (y + 3.0)**2 - 3.0


if __name__ == "__main__":

    model = om.Group()
    model.add_subsystem('parab_comp', Paraboloid())

    prob = om.Problem(model)
    prob.setup()

    prob.set_val('parab_comp.x', -1.0)
    prob.set_val('parab_comp.y', 7.0)

    prob.run_model()
    print(prob['parab_comp.f_xy'])
