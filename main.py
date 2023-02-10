#imports
from simulation import Inspector, Workstation

if __name__ =="__main__":

	print("Enter nothing for default simulation values (1000, 28000)")
	REPLICATIONS = int(input("Enter Replications: ") or "1000")
	REPLICATION_DURATION = int(input("Enter time (sec): ") or "28000")

	#import data from dat files
	inspector_1_data = [float(x)*60 for x in open('data/servinsp1.dat').read().splitlines() if x]
	inspector_2_data = [float(x)*60 for x in open('data/servinsp22.dat').read().splitlines() if x]
	inspector_3_data = [float(x)*60 for x in open('data/servinsp23.dat').read().splitlines() if x]

	workstation_1_data = [float(x)*60 for x in open('data/ws1.dat').read().splitlines() if x]
	workstation_2_data = [float(x)*60 for x in open('data/ws1.dat').read().splitlines() if x]
	workstation_3_data = [float(x)*60 for x in open('data/ws1.dat').read().splitlines() if x]

	#   Execution loop
    for iteration in range(1, REPLICATIONS+1):

        #   Environment
        logger.info('Starting iteration ' + str(iteration))
        main_env = simpy.Environment()
        REPLICATION_VARIABLES = ReplicationVariables(logger)

        # Class instantiations
        

        # Run simulation
        main_env.run(until=REPLICATION_DURATION)  # 'until' is simulation duration

        #   Save iteration variables
        # REPLICATION_OUTPUTS[iteration] = simulation_output.get_means()
        SIMULATION_VARIABLES.append(REPLICATION_VARIABLES)
        #   Simulation End
