# imports
from simulation import Inspector, Workstation
import simpy
from output_variables import SimulationOutputVariables
from os import *

if __name__ == "__main__":

    print("Enter nothing for default simulation values (1000, 28000)")
    REPLICATIONS = int(input("Enter Replications: ") or "1000")
    REPLICATION_DURATION = int(input("Enter time (sec): ") or "28000")

    simulation_output_variables = SimulationOutputVariables()

    # import data from dat files
    inspector_1_data = [
        float(x) * 60 for x in open("data/servinsp1.dat").read().splitlines() if x
    ]
    inspector_2_data = [
        float(x) * 60 for x in open("data/servinsp22.dat").read().splitlines() if x
    ]
    inspector_3_data = [
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
        env = simpy.Environment()

        # Class instantiations
        inspector_1 = Inspector("inspector_1", ["c1"], env, inspector_1_data)
        inspector_2 = Inspector("inspector_2", ["c2", "c3"], env, inspector_2_data)

        workstation_1 = Workstation("workstation_1", ["c1"], env, workstation_1_data)
        workstation_2 = Workstation(
            "workstation_2", ["c1", "c2"], env, workstation_2_data
        )
        workstation_3 = Workstation(
            "workstation_3", ["c1", "c3"], env, workstation_3_data
        )

        # Run simulation
        main_env.run(until=REPLICATION_DURATION)

        print(simulation_output_variables)
