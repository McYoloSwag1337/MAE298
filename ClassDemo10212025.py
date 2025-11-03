import openmdao.api as om
import numpy as np
import matplotlib as plt

class SimpleCost(om.ExplicitComponent):
    #do this for variables that you don't want the optimizer to turn into an Auto-IVC
    def initialize(self):
        self.options.declare('then_year', default=2030, types=int)
        
    def setup(self):
        #self.add_input('MTOW', val=10000)
        #self.add_input('then_year', val=2030)
        #self.add_input('cost', val=1.0e6)
        
    


#get everything from example
