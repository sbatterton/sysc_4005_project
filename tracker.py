#class to track components in the system throughout simulation
class Tracker(object):
    def __init__(self, env, inspectors, workstations, simulation_output_variables):
        self.env = env
        self.inspectors = inspectors
        self.workstations = workstations
        self.simulation_output_variables = simulation_output_variables
        self.action = env.process(self.run())

    def run(self):
        while True:
            components = {'c1': 0, 'c2': 0, 'c3': 0}
            for inspector in self.inspectors:
                if inspector.current:
                    components[inspector.current] += 1

            for workstation in self.workstations:

                #first get number of components in buffers
                for c in workstation.c:                    
                    components[c] += len(workstation.buffer[c].items)

                #then if they are in progress add another of each component they use
                if workstation.in_progress:
                    for c in workstation.c:
                        components[c] += 1

            self.simulation_output_variables.add_components(components)
            
            yield self.env.timeout(10)