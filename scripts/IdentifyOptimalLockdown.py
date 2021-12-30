# Edit path to import files
from time import time
from sys import path
path.insert(1, '../client_code/Simulation')

# Import files
from Simulation import Simulation
from Params import Params
from Utils import Utils
from Person import Person

# Set initial variables
baseline = 673
peakInfectedDay = 74
startDays = [-20, -15, -10, -5, 0]
lockdownLengths = [15, 30, 45, 60, 75]
simulationLength = 200
finalData = [[0 for _ in startDays] for _ in lockdownLengths]

# Calculate all values
for i, daysFromPeak in enumerate(startDays):
	for j, lockdownLength in enumerate(lockdownLengths):
		# Parameters for running the simulation
		lockdownStart = peakInfectedDay + daysFromPeak
		lockdownStop = lockdownStart + lockdownLength

		# Take average of 5 runs
		finalValue = 0
		runs = 5
		for _ in range(runs):
			params = Params(
				LOCKDOWN_ENABLED = True,
				LOCKDOWN_START = lockdownStart,
				LOCKDOWN_STOP = lockdownStop,
				SIMULATION_LENGTH = simulationLength
			)
			simulation = Simulation(params)
			startTime = time()
			
			# Run simulation
			peakInfection = 0
			frames = list(simulation.run())
			for frame in frames:
				if (peakInfection * 0.75 > len(frame.stateGroups[Person.INFECTED.id]) and 
					peakInfection >= 50):
					break
				peakInfection = frame.peakInfection

			print(lockdownStart, lockdownStop, peakInfection)
			# Utils.drawFramesMatplotlib(frames, params)
			finalValue += peakInfection
			print(f'Time taken: {time() - startTime:.2f}s')

		# Calculate final value 
		finalValue = int(round(finalValue / runs))
		print(finalValue)
		finalData[i][j] = finalValue

# Write data to csv file
with open('output.csv', 'w') as outputFile:
	# Write one row with start days
	outputFile.write(',' + ','.join(map(str, startDays)) + '\n')

	# Write other lines
	for i, row in enumerate(finalData):
		outputFile.write(str(lockdownLengths[i]) + ',' + ','.join(map(str, row)) + '\n')

# Visualize the data
exec(open('VisualizeLockdownHeatmap.py').read())
