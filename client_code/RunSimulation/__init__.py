from ._anvil_designer import RunSimulationTemplate
from anvil import *
import plotly.graph_objects as go

class RunSimulation(RunSimulationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def onRunSimulationButtonClick(self, **event_args):
    """This method is called when the button is clicked"""
    pass

