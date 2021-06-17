from ._anvil_designer import RunSimulationTemplate # type: ignore
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from plotly import graph_objects as go
from time import sleep

from ...Simulation.Simulation import Simulation
from ...Simulation.Person import Person
from ...Simulation.Params import Params

class RunSimulation(RunSimulationTemplate):
	"""Class which changes the UI in the RunSimulation form.
	
	Attributes
	----------
	canvasWidth : int
		The width of the canvas
	canvasHeight : int
		The height of the canvas
	timePerFrame : float
		The number of second each frame is displayed for
	graphXData : list(int)
		The data in the X axis of the graph
	graphYData : list(tuple(int))
		The data in the Y axis of the graph
	params : Params
		The parameters of the simulation

	Methods
	-------
	__init__(**properties)
		Initializes the run simulation form
	drawFrame(frame)
		Draws a frame on the UI
	"""

	def __init__(self, params = Params(), **properties):
		"""Initializes the run simulation
		
		Called when the RunSimulation form is created.
		Sets Form properties and Data Bindings and then
		runs any other code for initializing the form.

		Parameters
		----------
		params : Params
			The parameters of the simulation
		**properties
			The UI properties of the form
		
		Returns
		-------
		None
		"""
		
		self.init_components(**properties)
		
		# Any code you write here will run when the form opens.
		self.params = params
		
	def drawFrame(self, frame, frameCount):
		"""This method draws a frame on the canvas.
		
		For each frame, we are doing 2 things
		The first task is to draw each person in the frame 
		on the grid, in its appropriate color
		The second task is to plot the total number of people
		from each compartment on the graph in their respective colors

		Parameters
		----------
		frame
			The frame to draw
		frameCount
			The current frame count in the simulation
		
		Returns
		-------
		None
		"""
		
		# Initialize the canvas with a black, empty background
		self.canvas.background = 'black'
		self.canvas.clear_rect(0, 0, self.canvasWidth, self.canvasHeight)
		
		# Draw each person on the canvas as a dot with a particular color
		for person in frame.people:
			self.canvas.begin_path()
			self.canvas.arc(person.x * self.canvasWidth, person.y * self.canvasHeight, 5)
			self.canvas.fill_style = person.state.color
			self.canvas.fill()
		
		# Plot the result on the graph
		self.graphXData.append(frameCount)
		self.graph.data = []
		for stateID, stateCount in enumerate(frame.stateCounts):
			self.graphYData[stateID].append(stateCount)
			figure = go.Scatter(
				x = self.graphXData,
				y = self.graphYData[stateID],
				marker = dict(
					color = Person.states[stateID].color
				),
				name = Person.states[stateID].name
			)
			self.graph.data.append(figure)
		self.graph.data = self.graph.data

	def onRunSimulationButtonClick(self, **event_args):
		"""This method is called when the button is clicked
		
		Parameters
		----------
		**event_args
			Details about how the button is clicked
		
		Returns
		-------
		None
		"""

		# Initialize arrays for graphing the results
		self.graphXData = []
		self.graphYData = [[] for _ in Person.states]
		
		# Created a simulation object and runs the simulation
		simulation = Simulation(self.params)
		for frameCount, frame in enumerate(simulation.run()):
			self.drawFrame(frame, frameCount)
			sleep(self.params.TIME_PER_FRAME)
		

	def onCanvasShow(self, **event_args):
		"""This method is called when the Canvas is shown on the screen
		
		Initializes the canvas dimensions
		
		Parameters
		----------
		**event_args
			Details of the canvas
		
		Returns
		-------
		None
		"""
		
		self.canvasWidth = self.canvas.get_width()
		self.canvasHeight = self.canvas.get_height()
