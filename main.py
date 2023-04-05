# imports
from simulation import Inspector, Workstation
import simpy
from output_variables import SimulationOutputVariables
from tracker import Tracker

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

    #testing manual values
    '''
    inspector_1_data = [250]
    inspector_22_data = [1000]
    inspector_23_data = [1000]

    workstation_1_data = [1000]
    workstation_2_data = [1000]
    workstation_3_data = [1000]
    '''

    

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

        inspectors = [inspector_1, inspector_2]

        tracker = Tracker(env, inspectors, workstations, simulation_output_variables)

        # Run simulation
        env.run(until=REPLICATION_DURATION)

        #pretty printing

        #calculating number of components
        count = {'c1': sum(simulation_output_variables.products.values()), 'c2': simulation_output_variables.products[2], 'c3': simulation_output_variables.products[3]}
        #calculate average time components spend in the system
        average_time = {'c1': sum(simulation_output_variables.component_times['c1'])/count["c1"], 'c2': sum(simulation_output_variables.component_times['c2'])/count["c2"], 'c3': sum(simulation_output_variables.component_times['c3'])/count["c3"], 'total': sum([value for sublist in simulation_output_variables.component_times.values() for value in sublist])/len([value for sublist in simulation_output_variables.component_times.values() for value in sublist])}
        #calculate average count of ocmponents in system
        average_count = {'c1': sum(simulation_output_variables.components['c1'])/len(simulation_output_variables.components['c1']), 'c2': sum(simulation_output_variables.components['c2'])/len(simulation_output_variables.components['c2']), 'c3': sum(simulation_output_variables.components['c3'])/len(simulation_output_variables.components['c3'])}
        #calculate input rate to system
        input_rate = {'c1': count['c1']/REPLICATION_DURATION, 'c2': count['c2']/REPLICATION_DURATION, 'c3': count['c3']/REPLICATION_DURATION}
        #get average of  service times
        average_service_times = {
            "inspector_1": sum(simulation_output_variables.service_times['inspector_1'])/len(simulation_output_variables.service_times['inspector_1']),
            "inspector_2": sum(simulation_output_variables.service_times['inspector_2'])/len(simulation_output_variables.service_times['inspector_2']),
            "workstation_1": sum(simulation_output_variables.service_times['workstation_1'])/len(simulation_output_variables.service_times['workstation_1']),
            "workstation_2": sum(simulation_output_variables.service_times['workstation_2'])/len(simulation_output_variables.service_times['workstation_2']),
            "workstation_3": sum(simulation_output_variables.service_times['workstation_3'])/len(simulation_output_variables.service_times['workstation_3']),
        }
        #get percentage block time for inspectors and idle time for workstations
        percentage_block_time = {"inspector_1": (sum(simulation_output_variables.block_times['inspector_1'])/REPLICATION_DURATION)*100, "inspector_2": (sum(simulation_output_variables.block_times['inspector_2'])/REPLICATION_DURATION)*100}
        percentage_idle_time = {"workstation_1": (sum(simulation_output_variables.idle_times['workstation_1'])/REPLICATION_DURATION)*100, "workstation_2": (sum(simulation_output_variables.idle_times['workstation_2'])/REPLICATION_DURATION)*100, "workstation_3": (sum(simulation_output_variables.idle_times['workstation_3'])/REPLICATION_DURATION)*100}
        #calculate avergae buffer occupancy
        average_buffer_occupancy = {"workstation_1": {"c1": sum(simulation_output_variables.buffers["workstation_1"]["c1"])/len(simulation_output_variables.buffers["workstation_1"]["c1"])},
                                    "workstation_2": {"c1": sum(simulation_output_variables.buffers["workstation_2"]["c1"])/len(simulation_output_variables.buffers["workstation_2"]["c1"]), "c2": sum(simulation_output_variables.buffers["workstation_2"]["c2"])/len(simulation_output_variables.buffers["workstation_2"]["c2"])},
                                    "workstation_3": {"c1": sum(simulation_output_variables.buffers["workstation_3"]["c1"])/len(simulation_output_variables.buffers["workstation_3"]["c1"]), "c3": sum(simulation_output_variables.buffers["workstation_3"]["c3"])/len(simulation_output_variables.buffers["workstation_3"]["c3"])},    
                                    }

        #prints
        print("Number of Products Made:")
        print("P1:", simulation_output_variables.products[1])
        print("P2:", simulation_output_variables.products[2])
        print("P3:", simulation_output_variables.products[3])
        print("Total:", sum(simulation_output_variables.products.values()))
        print()

        print("Number of Components:")
        print("C1:", count['c1'])
        print("C2:", count['c2'])
        print("C3:", count['c3'])
        print("Total:", sum(count.values()))
        print()

        print("Average Time in System:")
        print("C1:", average_time['c1'])
        print("C2:", average_time['c2'])
        print("C3:", average_time['c3'])
        print("Total:", average_time['total'])
        print()

        print("Average Number in System:")
        print("C1:", average_count['c1'])
        print("C2:", average_count['c2'])
        print("C3:", average_count['c3'])
        print("Total:", sum(average_count.values()))
        print()

        print("Input Rate to System (units/second):")
        print("C1:", input_rate['c1'])
        print("C2:", input_rate['c2'])
        print("C3:", input_rate['c3'])
        print("Total:", sum(input_rate.values()))
        print()

        print("Average Service Times:")
        print("Inspector 1:", average_service_times['inspector_1'])
        print("Inspector 2:", average_service_times['inspector_2'])
        print("Workstation 1:", average_service_times['workstation_1'])
        print("Workstation 2:", average_service_times['workstation_2'])
        print("Workstation 3:", average_service_times['workstation_3'])
        print()
        
        print("Percentage Block Time:")
        print(f"Inspector 1: {percentage_block_time['inspector_1']}%")
        print(f"Inspector 2: {percentage_block_time['inspector_2']}%")
        print()

        print("Percentage Idle Times:")
        print(f"Workstation 1: {percentage_idle_time['workstation_1']}%")
        print(f"Workstation 2: {percentage_idle_time['workstation_2']}%")
        print(f"Workstation 3: {percentage_idle_time['workstation_3']}%")
        print()

        print("Average Buffer Occupancy:")
        print("Workstation 1, C1:", average_buffer_occupancy["workstation_1"]["c1"])
        print("Workstation 2, C1:", average_buffer_occupancy["workstation_2"]["c1"])
        print("Workstation 2, C2:", average_buffer_occupancy["workstation_2"]["c2"])
        print("Workstation 3, C1:", average_buffer_occupancy["workstation_3"]["c1"])
        print("Workstation 3, C3:", average_buffer_occupancy["workstation_3"]["c3"])

        #printing out product average times
        """
        for i, p in enumerate(simulation_output_variables.product_times[1]):
            print(p/(i+1))
        print("#####################################################################################")
        for i, p in enumerate(simulation_output_variables.product_times[2]):
            print(p/(i+1))
        print("#####################################################################################")
        for i, p in enumerate(simulation_output_variables.product_times[3]):
            print(p/(i+1))
        """
        