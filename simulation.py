from simpy.resources import container, store
from random import choice

class Inspector(object):
    def __init__(self, name, c, env, data, simulation_output_variables, workstations):
        self.name = name  # name of the inspector
        self.c = c  # will be just [c1] for inspector 1 and [c2, c3] for inspector 2
        self.env = env
        self.data = data
        self.simulation_output_variables = simulation_output_variables
        self.workstations = workstations
        self.action = env.process(self.run())

    def run(self):
        while True:
            component_start_time = self.env.now
            if self.name == "inspector_1":
                service_time = choice(self.data)
                self.simulation_output_variables.add_service_time(
                    self.name, service_time
                )

                yield self.env.timeout(service_time)
                block_time = self.env.now

                #wait for there to be space in one of the buffers
                while len(self.workstations[0].buffer["c1"].items) == 2 and len(self.workstations[1].buffer["c1"].items) == 2 and len(self.workstations[2].buffer["c1"].items) == 2:
                    yield self.env.timeout(0.1)
                
                #if ws1 has less or equal to ws2, and ws1 has less or equal to ws3, put in ws1
                if len(self.workstations[0].buffer["c1"].items) <= len(self.workstations[1].buffer["c1"].items) and len(self.workstations[0].buffer["c1"].items) <= len(self.workstations[2].buffer["c1"].items):
                    yield self.workstations[0].buffer["c1"].put(['c1', component_start_time])
                    # print("Added component 1 to workstation 1 buffer")

                #if ws2 has less or equal to ws3 put in ws2
                elif len(self.workstations[1].buffer["c1"].items) <= len(self.workstations[2].buffer["c1"].items):
                    yield self.workstations[1].buffer["c1"].put(['c1', component_start_time])
                    # print("Added component 1 to workstation 2 buffer")

                #put in ws3
                else:
                    yield self.workstations[2].buffer["c1"].put(['c1', component_start_time])
                    # print("Added component 1 to workstation 3 buffer")
                self.simulation_output_variables.add_block_time(self.name, self.env.now - block_time)
            else:
                if choice(self.c) == "c2":  # Randomly decides which component to make
                    service_time = choice(self.data[0])
                    self.simulation_output_variables.add_service_time(
                        self.name, service_time
                    )
                    yield self.env.timeout(service_time)
                    block_time = self.env.now
                    while len(self.workstations[1].buffer["c2"].items) == 2:
                        yield self.env.timeout(0.1)
                    yield self.workstations[1].buffer["c2"].put(['c2', component_start_time])
                    self.simulation_output_variables.add_block_time(self.name, self.env.now - block_time)
                    # print("Added component 2 to workstation 2 buffer")
                else:
                    service_time = choice(self.data[1])
                    self.simulation_output_variables.add_service_time(
                        self.name, service_time
                    )
                    yield self.env.timeout(service_time)
                    block_time = self.env.now
                    while len(self.workstations[2].buffer["c3"].items) == 2:                            
                        yield self.env.timeout(0.1)
                    yield self.workstations[2].buffer["c3"].put(['c3', component_start_time])
                    self.simulation_output_variables.add_block_time(self.name, self.env.now - block_time)
                    # print("Added component 3 to workstation 3 buffer")


class Workstation(object):
    def __init__(self, name, c, env, data, simulation_output_variables):
        self.name = name  # name of the Workstation
        self.c = c  # will be [c1], [c1, c2], [c1, c3]
        self.env = env
        self.data = data
        self.buffer = {}
        for n in c:
            self.buffer[n] = store.Store(self.env, 2)
        self.simulation_output_variables = simulation_output_variables
        self.action = env.process(self.run())

    def run(self):
        while True:
            idle_start = self.env.now
            components = []
            #workstation 1
            if len(self.c) == 1:
                component = yield self.buffer[self.c[0]].get()
                components.append(component)
            #workstation 2 and 3
            else:
                component = yield self.buffer[self.c[0]].get()
                components.append(component)
                component = yield self.buffer[self.c[1]].get()
                components.append(component)
            self.simulation_output_variables.add_idle_time(
                self.name, self.env.now - idle_start
            )
            service_time = choice(self.data)
            self.simulation_output_variables.add_service_time(self.name, service_time)
            yield self.env.timeout(service_time)
            for component in components:
                self.simulation_output_variables.add_component_time(component[0], self.env.now - component[1])
            self.simulation_output_variables.add_product(int(self.name[-1]))
            # print(f"Product {int(self.name[-1])} assembled")
