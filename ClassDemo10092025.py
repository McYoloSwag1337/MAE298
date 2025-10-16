#following along
#split components from run script
import numpy as np
import openmdao.api as om

class SellarDis1(om.ExplicitComponent):
    #Discipline 1 for the sellar Example
    #y1 = z1^2 + x + z2 - 0.2*y2
    def setup(self):
        #design variables
        self.add_input('z', val=np.zeros(2))
        self.add_input('x', val=0.0)
        #coupling parameter
        self.add_input('y2', val=1.0)
        #output
        self.add_output('y1', val=1.0)
        
        #equivalent to below
        #self.declare_partials('y1', ['z','x'z'y2'])
    
    def setup_partials(self):
        self.declare_partials('*','*', method='fd') 
        #can switch to constant steps 'cs'
        
    def compute(self, inputs, outputs):
        z1 = inputs['z'][0]
        z2 = inputs['z'][1]
        x1 = inputs['x'][0]
        y2 = inputs['y2'][0]
        
        outputs['y1'] = z1**2 +z2 +x1 - 0.2*y2
        
    # ^ This is our first discipline ^
    
    
    
class SellarDis2(om.ExplicitComponent):
    #Discipline 2 for the sellar Example
    #y2 = sqrt(y1) + z1 + z2
    def setup(self):
        #design variables
        self.add_input('z', val=np.zeros(2))
        self.add_input('y1', val=1.0)
        #output
        self.add_output('y2', val=1.0)
      
    
    def setup_partials(self):
        self.declare_partials('*','*', method='fd') #can switch to complex steps 'cs'
        
    def compute(self, inputs, outputs):
        z1 = inputs['z'][0]
        z2 = inputs['z'][1]
        y1 = inputs['y2'][0]
        
        outputs['y2'] = y1**0.5 +z1 +z2 
        #caution, complex number can occur from negative in sqrt
        #this is bad practice but we will put a fake bound on it
        #bad practice because it artificially limits the solution space
        
        if y1.real < 0.0:
            y1 *= -1
        
    # ^ This is our second discipline ^
    # now we are going to group these components
    
class SellarMDAConnect(om.Group):
    
    def setup(self):
        #defining independent variables. promote be the easier way of doing this
        indvar = self.add_subsystem('indvar', om.IndepVarComp())
        indvar.add_output('x', val=1.0)
        indvar.add_output('z', val=np.array([5.0,2.0]))
        
        #couple the cycle with a non-linear solver
        #calling an empty subsystem
        cycle = self.add_subsystem('cycle', om.Group())
        
        #now that it exists we will add to it also rename
        cycle.add_subsystem('d1', SellarDis1())
        cycle.add_subsystem('d2', SellarDis2())
        
        #couple cycles together. could have done this later where the wiring happens
        cycle.connect('d1.y1', 'd2,y1')
       
        cycle.connect('d2.y2', 'd1,y2')
        #^equivalent to  self.connect(src_name:'cycle.d2.y2', tgt_name:['cycle.d1.y2','obj.cmp.y2', 'con_cmp1.y2'])^
        
        #now we will tell it how to solve nonlinear
        cycle.nonlinear_solver = om.NonlinearBlockGS()
        
        #currently all they know is that they are in the same group but dont know anything else about each other
        
        #objective function definition
        self.add_subsystem('obj_cmp', om.ExecComp('obj = x**2 + z[1] +y1 + exp(-y2)', z=np.zeros(2), x=0.0))
        self.add_subsystem('con_cmp1', om.ExecComp('con1=3.16-y1'))
        self.add_subsystem('con_cmp2', om.ExecComp('con2=y2-24.8'))
        
        #wire this group together (let them know each other)
        #telling openmdao that the variables are connected to each other
        #literally telling each box what their inputs and outputs are and linking the outputs of some to inputs of others
        self.connect('indvar.x', ['cycle.d1.x', 'obj_cmp.x'])
        self.connect('indvar.z', ['cycle.d1.z', 'cycle.d2.z', 'obj_cmp.z'])
        self.connect('cycle.d1.y1', ['obj.cmp.y1', 'con_cmp1.y1'])
        self.connect('cycle.d2.y2', ['obj.cmp.y2', 'con_cmp2.y2'])
        
        
#how to do simple promotions
#names are important. link by names

class SellarMDA_simplepromote(om.Group):
    def setup(self):
        
        cycle=self.add_subsystem('cycle', om.Group(), promotes=['*'])
        cycle.add_subsystem('d1', SellarDis1(), promotes_inputs=['x', 'z', 'y2'], promotes_outputs=['y1'])
        cycle.add_subsystem('d2', SellarDis2(), promotes_inputs=['z', 'y1'], promotes_outputs=['y1\2'])
        
        #instead of s
        
        cycle.set_input_defaults('x', 1.0)
        cycle.set_input_defaults('z', np.array([5.0, 2.0]))
        
        cycle.nonlinear_solver = om.NonlinearBlockGS()
        
        #build in objective and constraints
        #everything is unfinished below!!!
        
        self.add_subsystem('obj_cmp', om.ExecComp('obj = x**2 +z[1] +y1 + exp(-y2)'), z=np.array([0.0,0.0]), x=0.0), promotes['x','z','y1','y2,' ]
        
        self.add_subsystem('con_cmp1', om.ExecComp('con1=3.16'-y1))
        self.add_subsystem('con_cmp2', om.ExecComp('con2=y2-24.0'), promotes=[])
        

