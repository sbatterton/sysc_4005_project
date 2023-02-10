class Inspector(object):

    def __init__(self, n, c, env, simulation_variables):
        self.n = n #number of the Inspector
        self.c = c #will be just [c1] for inspector 1 and [c2, c3] for inspector 2
        self.env = env
        self.action = env.process(self.run())
        self.simulation_variables = simulation_variables
    
    def run(self):
        while True:
            pass

class Workstation(object):

    def __init__(self, n, c, env, simulation_variables):
        self.n = n #number of the Workstation
        self.c = c #will be [c1], [c1, c2], [c1, c3]
        self.env = env
        self.simulation_variables = simulation_variables
        self.action = env.process(self.run())
        self.buffers = [[None]*2]*len(c)    #will make the buffers depending on c input, either 
        #[[None, None]], or [[None, None], [None, None]], with indices corresponding to c list
    
    def run(self):
        while True:
            pass
