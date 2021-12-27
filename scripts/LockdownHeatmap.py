# Import csv reader and plotly
from csv import reader
# from scipy.ndimage.filters import gaussian_filter
# from plotly import graph_objects as go
# import seaborn as sns
from matplotlib import pyplot as plt

def displayHeatMap(xAxis, yAxis, zAxis, msg):
	# Display a heatmap representing the data
	# Matplotlib
	fig, ax = plt.subplots()
	heatmap = plt.imshow(
		zAxis,
		cmap = 'autumn',
		interpolation = 'bilinear',
		extent = [xAxis[0], xAxis[-1], yAxis[0], yAxis[-1]],
		aspect = 'auto'
		# vmin = 0,
		# vmax = 100
	)
	plt.title(msg)	
	plt.xlabel('Lockdown start (Days before peak)')
	plt.ylabel('Lockdown length')
	plt.colorbar(heatmap)
	plt.show()

# Read data from input file
inputFile = input('Enter file path: ')
with open(inputFile) as f:
	csvReader = reader(f)
	fileData = list(csvReader)
	xAxis = list(map(int, fileData[0][1:]))
	yAxis = [int(row[0]) for row in fileData[1:]]
	data = [list(map(float, row[1:])) for row in fileData[1:]]
	data = data[::-1]
	print(data)

# Calculate values
# Percentage reduction in peak hospitalization
baseline = float(input('Enter baseline value: '))
zAxis1 = [[(baseline - x) / baseline * 100 for x in row] for row in data]
displayHeatMap(
	xAxis,
	yAxis,
	zAxis1,
	'Reduction in peak hospital cases under different lockdown conditions'
)

# Percentage reduction in peak hospitalization per day of lockdown
zAxis2 = [[x / yAxis[-i - 1] for x in row] for i, row in enumerate(zAxis1)]
displayHeatMap(
	xAxis,
	yAxis,
	zAxis2,
	'Reduction in peak hospital cases per day of lockdown'
)
