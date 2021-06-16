from ._anvil_designer import RunSimulationTemplate # type: ignore
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from plotly import graph_objects as go
from time import sleep

from ...Simulation.Simulation import Simulation
from ...Simulation.Person import Person

class RunSimulation(RunSimulationTemplate):
  """Class which changes the UI in the RunSimulation form.
  
  Attributes
  ----------
  width : int
    The width of the canvas
  height : int
    The height of the canvas
  timePerFrame : float
    The number of second each frame is displayed for
  graphXData : list(int)
    The data in the X axis of the graph
  graphYData : list(tuple(int))
    The data in the Y axis of the graph

  Methods
  -------
  __init__(**properties)
    Initializes the run simulation form
  drawFrame(frame)
    Draws a frame on the UI
  """

  def __init__(self, **properties):
    """Initializes the run simulation
    
    Called when the RunSimulation form is created.
    Sets Form properties and Data Bindings and then
    runs any other code for initializing the form.

    Parameters
    ----------
    **properties
      The UI properties of the form
    
    Returns
    -------
    None
    """
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.timePerFrame = 0.5
    
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
    self.canvas.clear_rect(0, 0, self.width, self.height)
    
    '''# Draw each person on the canvas as a dot with a particular color
    for person in frame.people:
      self.canvas.begin_path()
      self.canvas.arc(person.x * self.width, person.y * self.height, 5)
      self.canvas.fill_style = person.state.color
      self.canvas.fill()
    
    # Plot the result on the graph
    self.graphXData.append(frameCount)
    for stateID, stateCount in frame.stateCounts:
      self.graphYData[stateID].append(stateCount)
      figure = go.Figure(
        data = go.Scatter(
          x = self.graphXData,
          y = self.graphYData[stateID]
        ),
        color = Person.states[stateID].color
      )
      self.graph.data = [figure]'''

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
    simulation = Simulation()
    for frameCount, frame in enumerate(simulation.run()):
      self.drawFrame(frame, frameCount + 1)
      sleep(self.timePerFrame)

  def onCanvasShow(self, **event_args):
    """This method is called when the Canvas is shown on the screen"""
    # Initialize the canvas dimensions
    self.width = self.canvas.get_width()
    self.height = self.canvas.get_height()
    print(self.width, self.height)
