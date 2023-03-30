# imports
from simulation import Inspector, Workstation
import simpy
from output_variables import SimulationOutputVariables

if __name__ == "__main__":

    REPLICATIONS = 1
    REPLICATION_DURATION = 1000000

    # import data from dat files
    inspector_1_data = [
        float(x) * 60 for x in open("data/servinsp1.dat").read().splitlines() if x
    ]
    inspector_22_data = [
        float(x) * 60 for x in open("data/servinsp22.dat").read().splitlines() if x
    ]
    inspector_23_data = [
        float(x) * 60 for x in open("data/servinsp23.dat").read().splitlines() if x
    ]

    workstation_1_data = [
        float(x) * 60 for x in open("data/ws1.dat").read().splitlines() if x
    ]
    workstation_2_data = [
        float(x) * 60 for x in open("data/ws1.dat").read().splitlines() if x
    ]
    workstation_3_data = [
        float(x) * 60 for x in open("data/ws1.dat").read().splitlines() if x
    ]

    #   Execution loop
    for iteration in range(1, REPLICATIONS + 1):

        #   Environment
        # print("Creating Simulation Environment")
        env = simpy.Environment()

        simulation_output_variables = SimulationOutputVariables()

        # Class instantiations
        workstation_1 = Workstation(
            "workstation_1",
            ["c1"],
            env,
            workstation_1_data,
            simulation_output_variables,
        )
        workstation_2 = Workstation(
            "workstation_2",
            ["c1", "c2"],
            env,
            workstation_2_data,
            simulation_output_variables,
        )
        workstation_3 = Workstation(
            "workstation_3",
            ["c1", "c3"],
            env,
            workstation_3_data,
            simulation_output_variables,
        )

        workstations = [workstation_1, workstation_2, workstation_3]

        inspector_1 = Inspector(
            "inspector_1",
            ["c1"],
            env,
            inspector_1_data,
            simulation_output_variables,
            workstations,
        )
        inspector_2 = Inspector(
            "inspector_2",
            ["c2", "c3"],
            env,
            [inspector_22_data, inspector_23_data],
            simulation_output_variables,
            workstations,
        )

        # Run simulation
        env.run(until=REPLICATION_DURATION)

        # print(simulation_output_variables.service_times)
        # print(simulation_output_variables.idle_times)
        # print(simulation_output_variables.block_times)
        # print(simulation_output_variables.component_times)
        print(simulation_output_variables.products)
