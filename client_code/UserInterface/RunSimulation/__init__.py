from ._anvil_designer import RunSimulationTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
from time import sleep

from ...Simulation import Simulation

class RunSimulation(RunSimulationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    
  def drawFrame(self, frame):
    '''This method draws a frame on the canvas'''
    self.canvas.background = 'black'
    s
    for person in frame.people:
      self.canvas.arc(person.x, person.y, 5)
      self.canvas.fill_style = 'blue'
      self.canvas.fill()

  def onRunSimulationButtonClick(self, **event_args):
    '''This method is called when the button is clicked'''
    frame = Simulation.getFrame()
    self.drawFrame(frame)