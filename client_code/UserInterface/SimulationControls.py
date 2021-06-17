from ._anvil_designer import SimulationControlsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..Simulation.Params import Params

class SimulationControls(SimulationControlsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.populationSizeSlider.default = Params.POPULATION_SIZE
    self.populationSizeLabel.text = f'Population Size (10 - 1000): {Params.POPULATION_SIZE}'
    

  def onPopulationSizeSliderChange(self, **event_args):
    """This method is called when the population size slider is moved"""
    self.populationSizeLabel.text = f'Population Size (10 - 1000): {self.populationSizeSlider.level}'
