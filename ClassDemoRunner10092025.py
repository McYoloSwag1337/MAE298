import openmdao.api as om
import ClassDemo10092025 as dsc

#set up the problem 

prob = om.Problem()
prob.model = dsc.SellarMDAConnect()

#prob.setup()

#prob.set_val('indvar.x', 2.0)
#prob.set_val('indvar.z',[-1., -1.])

#prob.run_model()

##n2 diagram maker
#om.n2(prob)

#lets make this an optimizer instead of a solver
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'
prob.driver.options['maxiter'] = 100
prob.driver.options['tol'] = 1.0e-8

# add design variables
prob.model.add_design_var('x', lower=0., upper=10.)
prob.model.add_design_var('x', lower=0., upper=10.)

prob.model.add_constraint('con1', upper=0.)
prob.model.add_constraint('con2', upper=0.)

prob.model.approx_totals()

prob.set_solver_print(levl=0)

prob.setup()

prob.run_driver()

print('minimum found at')
print(prob.get_val('x'))
print(prob.get_val('x'))

#print(f"y1 = {prob.get_val('cycle.d1.y1')}, y2 = {prob.get_val('cycle.d2.y2')}") 