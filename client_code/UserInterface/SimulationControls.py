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
    # Initalize all the options based on the default values of Params
    self.params = Params()
    
    self.populationSizeSlider.default = self.params.POPULATION_SIZE
    self.populationSizeLabel.text = f'Population Size (10 - 1000): {self.populationSizeSlider.default}'
    
    self.simulationLengthSlider.default = self.params.SIMULATION_LENGTH
    self.simulationLengthLabel.text = f'Simulation Length (10 - 500): {self.simulationLengthSlider.default}'
    
    self.infectionRateSlider.default = int(self.params.INFECTION_RATE * 100)
    self.infectionRateLabel.text = f'Infection Rate (1 - 100): {self.infectionRateSlider.default}'
    
  def onPopulationSizeChange(self, **event_args):
    """This method is called when the population size slider is moved"""
    self.params.POPULATION_SIZE = self.populationSizeSlider.level
    self.populationSizeLabel.text = f'Population Size (10 - 1000): {self.populationSizeSlider.level}'

  def onSimulationLengthChange(self, **event_args):
    """This method is called when the simulation length slider is moved"""
    self.params.SIMULATION_LENGTH = self.simulationLengthSlider.level
    self.simulationLengthLabel.text = f'Simulation Length (10 - 500): {self.simulationLengthSlider.level}'

  def onInfectionRateChange(self, **event_args):
    """This method is called when the infection rate slider is moved"""
    self.params.INFECTION_RATE = self.infectionRateSlider.level / 100
    self.infectionRateLabel.text = f'Infection Rate (1 - 100): {self.infectionRateSlider.level}'

