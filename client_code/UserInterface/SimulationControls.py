from ._anvil_designer import SimulationControlsTemplate # type: ignore
from anvil import *
import plotly.graph_objects as go
import anvil.server

from ..Simulation.Params import Params

class SimulationControls(SimulationControlsTemplate):
  """Class which changes the UI in the RunSimulation form.

  Attributes
  ----------
  params : Params
    The parameters of the simulation
  
  Methods
  -------
  __init__(**properties)
    Initializes the run simulation form
  """

  def __init__(self, **properties):
    """Initializes the run simulation
    
    Called when the SimulationControls form is created.
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
    # Initalize all the options based on the default values of Params
    self.params = Params()
    
    self.populationSizeSlider.default = self.params.POPULATION_SIZE
    self.populationSizeLabel.text = f'Population Size (10 - 1000): {self.populationSizeSlider.default}'
    
    self.simulationLengthSlider.default = self.params.SIMULATION_LENGTH
    self.simulationLengthLabel.text = f'Simulation Length (10 - 500): {self.simulationLengthSlider.default}'
    
    self.infectionRateSlider.default = int(self.params.INFECTION_RATE * 100)
    self.infectionRateLabel.text = f'Infection Rate (1 - 100): {self.infectionRateSlider.default}'
  
    self.incubationPeriodSlider.default = self.params.INCUBATION_PERIOD
    self.incubationPeriodLabel.text = f'Incubation Period (1 - 100): {self.incubationPeriodSlider.default}'
    
    self.infectionPeriodSlider.default = self.params.INFECTION_PERIOD
    self.infectionPeriodLabel.text = f'Infection Period (1 - 100): {self.infectionPeriodSlider.default}'
    
    self.mortalityRateSlider.default = int(self.params.MORTALITY_RATE * 100)
    self.mortalityRateLabel.text = f'Mortality Rate (1 - 100): {self.mortalityRateSlider.default}'
    
  def onPopulationSizeChange(self, **event_args):
    """This method is called when the population size slider is moved"""
    self.params.POPULATION_SIZE = self.populationSizeSlider.level
    self.populationSizeLabel.text = f'Population Size (10 - 1000): {self.populationSizeSlider.level}'

  def onSimulationLengthChange(self, **event_args):
    """This method is called when the simulation length slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the button is clicked
    
    Returns
    -------
    None"""

    self.params.SIMULATION_LENGTH = self.simulationLengthSlider.level
    self.simulationLengthLabel.text = f'Simulation Length (10 - 500): {self.simulationLengthSlider.level}'

  def onInfectionRateChange(self, **event_args):
    """This method is called when the infection rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the button is clicked
    
    Returns
    -------
    None"""

    self.params.INFECTION_RATE = self.infectionRateSlider.level / 100
    self.infectionRateLabel.text = f'Infection Rate (1 - 100): {self.infectionRateSlider.level}'

  def onIncubationPeriodChange(self, **event_args):
    """This method is called when the incubation period slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the button is clicked
    
    Returns
    -------
    None"""

    self.params.INCUBATION_PERIOD = self.incubationPeriodSlider.level
    self.incubationPeriodLabel.text = f'Incubation Period (1 - 100): {self.incubationPeriodSlider.level}'

  def onInfectionPeriodChange(self, **event_args):
    """This method is called when the infection period slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the button is clicked
    
    Returns
    -------
    None"""

    self.params.INCUBATION_PERIOD = self.incubationPeriodSlider.level
    self.incubationPeriodLabel.text = f'Infection Period (1 - 100): {self.incubationPeriodSlider.level}'

  def onMortalityRateChange(self, **event_args):
    """This method is called when the mortality rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the button is clicked
    
    Returns
    -------
    None"""
    
    self.params.INFECTION_RATE = self.mortalityRateSlider.level / 100
    self.mortalityRateLabel.text = f'Mortality Rate (1 - 100): {self.mortalityRateSlider.level}'
    