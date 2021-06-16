from ._anvil_designer import RunSimulationTemplate # type: ignore
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go

from ...Simulation.Simulation import Simulation

class RunSimulation(RunSimulationTemplate):
  """Class which changes the UI in the RunSimulation form.
  
  Attributes
  ----------
  width : int
    The width of the canvas
  height : int
    The height of the canvas

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
    # Initialize the canvas dimensions
    self.width = 460
    self.height = 460
    
    
  def drawFrame(self, frame):
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
    
    Returns
    -------
    None
    """
    
    print('Debug')

    # Initialize the canvas with a black background
    self.canvas.background = 'black'
    
    # Draw each person on the canvas as a dot
    for person in frame.people:
      print(person.x, person.y)
      self.canvas.arc(person.x * self.width, person.y * self.height, 5)
      self.canvas.fill_style = person.state.color
      self.canvas.fill()

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
    
    # Created a simulation object and runs the simulation
    simulation = Simulation()
    i = 0
    for frame in simulation.run():
      self.drawFrame(frame)