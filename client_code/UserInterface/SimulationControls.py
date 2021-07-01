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
    
    self.populationSizeSlider.start = self.params.POPULATION_SIZE
    self.populationSizeLabel.text = f'Population Size (10 - 1000): {self.populationSizeSlider.start}'
    
    self.simulationLengthSlider.start = self.params.SIMULATION_LENGTH
    self.simulationLengthLabel.text = f'Simulation Length (10 - 500): {self.simulationLengthSlider.start}'
    
    self.infectionRateSlider.start = int(self.params.INFECTION_RATE * 100)
    self.infectionRateLabel.text = f'Infection Rate (1 - 100): {self.infectionRateSlider.start}'
  
    self.incubationPeriodSlider.start = self.params.INCUBATION_PERIOD
    self.incubationPeriodLabel.text = f'Incubation Period (1 - 100): {self.incubationPeriodSlider.start}'
    
    self.infectionPeriodSlider.start = self.params.INFECTION_PERIOD
    self.infectionPeriodLabel.text = f'Infection Period (1 - 100): {self.infectionPeriodSlider.start}'
    
    self.mortalityRateSlider.start = int(self.params.MORTALITY_RATE * 100)
    self.mortalityRateLabel.text = f'Mortality Rate (1 - 100): {self.mortalityRateSlider.start}'
    
    self.vaccinationSwitch.checked = self.params.VACCINATION_ENABLED
    
  def onPopulationSizeChange(self, **event_args):
    """This method is called when the population size slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    """
    
    self.params.POPULATION_SIZE = self.populationSizeSlider.value
    self.populationSizeLabel.text = f'Population Size (10 - 1000): {self.populationSizeSlider.value}'

  def onSimulationLengthChange(self, **event_args):
    """This method is called when the simulation length slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    """

    self.params.SIMULATION_LENGTH = self.simulationLengthSlider.value
    self.simulationLengthLabel.text = f'Simulation Length (10 - 500): {self.simulationLengthSlider.value}'

  def onInfectionRateChange(self, **event_args):
    """This method is called when the infection rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    """

    self.params.INFECTION_RATE = self.infectionRateSlider.value / 100
    self.infectionRateLabel.text = f'Infection Rate (1 - 100): {self.infectionRateSlider.value}'

  def onIncubationPeriodChange(self, **event_args):
    """This method is called when the incubation period slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    """

    self.params.INCUBATION_PERIOD = self.incubationPeriodSlider.value
    self.incubationPeriodLabel.text = f'Incubation Period (1 - 100): {self.incubationPeriodSlider.value}'

  def onInfectionPeriodChange(self, **event_args):
    """This method is called when the infection period slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    """

    self.params.INFECTION_PERIOD = self.incubationPeriodSlider.value
    self.infectionPeriodLabel.text = f'Infection Period (1 - 100): {self.incubationPeriodSlider.value}'

  def onMortalityRateChange(self, **event_args):
    """This method is called when the mortality rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    """
    
    self.params.INFECTION_RATE = self.mortalityRateSlider.value / 100
    self.mortalityRateLabel.text = f'Mortality Rate (1 - 100): {self.mortalityRateSlider.value}'
    
  def onVaccinationSwitchChange(self, **event_args):
    """This method is called when this switch is checked or unchecked
    
    Parameters
    ----------
    **event_args
      Details about how the switch is checked
    
    Returns
    -------
    None
    """
    
    self.params.VACCINATION_ENABLED = not self.params.VACCINATION_ENABLED

  def onRuleComplianceRateChange(self, handle, **event_args):
    """"This method is called when the rule compliance rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    """
    
    self.params.FOLLO
