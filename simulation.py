class Inspector(object):

    def __init__(self, c, env, simulation_variables, workstations):
		self.c = c
        self.env = env
		self.action = env.process(self.run())
        self.simulation_variables = simulation_variables        
        self.workstations = workstations