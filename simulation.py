from simpy.resources import container
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
            if self.name == "inspector_1":
                service_time = choice(self.data)
                self.simulation_output_variables.add_service_time(
                    self.name, service_time
                )
                yield self.env.timeout(service_time)
                block_time = self.env.now
                if (
                    self.workstations[0].buffer["c1"].level
                    <= self.workstations[1].buffer["c1"].level
                    or self.workstations[0].buffer["c1"].level
                    <= self.workstations[2].buffer["c1"].level
                ):
                    yield self.workstations[0].buffer["c1"].put(1)
                    # print("Added component 1 to workstation 1 buffer")

                elif (
                    self.workstations[1].buffer["c1"].level
                    <= self.workstations[2].buffer["c1"].level
                ):
                    yield self.workstations[1].buffer["c1"].put(1)
                    # print("Added component 1 to workstation 2 buffer")

                else:
                    yield self.workstations[2].buffer["c1"].put(1)
                    # print("Added component 1 to workstation 3 buffer")
            else:
                while True:
                    if (
                        choice(self.c) == "c2"
                    ):  # Randomly decides which component to make
                        service_time = choice(self.data[0])
                        self.simulation_output_variables.add_service_time(
                            self.name, service_time
                        )
                        yield self.env.timeout(service_time)
                        block_time = self.env.now
                        yield self.workstations[1].buffer["c2"].put(1)
                        # print("Added component 2 to workstation 2 buffer")
                    else:
                        service_time = choice(self.data[1])
                        self.simulation_output_variables.add_service_time(
                            self.name, service_time
                        )
                        yield self.env.timeout(service_time)
                        block_time = self.env.now
                        yield self.workstations[2].buffer["c3"].put(1)
                        # print("Added component 3 to workstation 3 buffer")
            self.simulation_output_variables.add_block_time(
                self.name, self.env.now - block_time
            )


class Workstation(object):
    def __init__(self, name, c, env, data, simulation_output_variables):
        self.name = name  # name of the Workstation
        self.c = c  # will be [c1], [c1, c2], [c1, c3]
        self.env = env
        self.data = data
        self.buffer = {}
        for n in c:
            self.buffer[n] = container.Container(self.env, 2)
        self.simulation_output_variables = simulation_output_variables
        self.action = env.process(self.run())

    def run(self):
        while True:
            idle_start = self.env.now
            if len(self.c) == 1:
                yield self.buffer[self.c[0]].get(1)
            else:
                yield self.buffer[self.c[0]].get(1) & self.buffer[self.c[1]].get(1)
            self.simulation_output_variables.add_idle_time(
                self.name, self.env.now - idle_start
            )
            service_time = choice(self.data)
            self.simulation_output_variables.add_service_time(self.name, service_time)
            yield self.env.timeout(service_time)
            self.simulation_output_variables.add_product(int(self.name[-1]))
            # print(f"Product {int(self.name[-1])} assembled")
