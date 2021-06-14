from ._anvil_designer import MainTemplate
from anvil import *

from ..RunSimulation import RunSimulation
from ..SimulationControls import SimulationControls

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def onSimulationControlsLinkClick(self, **event_args):
    """This method is called when the simulation controls link in the navbar is clicked"""
    self.root.clear()
    self.root.add_component(SimulationControls())

  def onSimulationLinkClick(self, **event_args):
    """This method is called when the simulation link in the navbar is clicked"""
    self.root.clear()
    self.root.add_component(RunSimulation())