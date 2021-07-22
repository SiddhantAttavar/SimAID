from ._anvil_designer import SimulationControlsTemplate # type: ignore
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
import anvil.server

from ..Simulation.Params import Params

class SimulationControls(SimulationControlsTemplate):
  '''Class which changes the UI in the RunSimulation form.

  Attributes
  ----------
  params : Params
    The parameters of the simulation
  
  Methods
  -------
  __init__(**properties)
    Initializes the run simulation form
  '''

  def __init__(self, **properties):
    '''Initializes the simulation controls page
    
    Called when the SimulationControls form is created.
    Sets Form properties and Data Bindings and then
    runs any other code for initializing the form.

    Parameters
    ----------
    **properties : dict
      The UI properties of the form
    
    Returns
    -------
    None
    '''

    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    # Initalize all the options based on the default values of Params
    self.params = Params()
    
    self.populationSizeSlider.start = self.params.POPULATION_SIZE
    self.populationSizeLabel.text = f'Population Size (10 - 1000): {self.populationSizeSlider.start}'
    
    demographicsStart = [round(i * 100) for i in self.params.POPULATION_DEMOGRAPHICS]
    self.populationDemographicsSlider.start = demographicsStart
    self.populationDemographicsSlider.connect = [True, False, True, False]
    self.populationDemographicsLabel.text = f'''Population Demographics: 
    0 - 15: {demographicsStart[0]}
    15 - 45: {demographicsStart[1] - demographicsStart[0]}
    45 - 65: {demographicsStart[2] - demographicsStart[1]}
    65+: {demographicsStart[3] - demographicsStart[2]}'''
    
    self.simulationLengthSlider.start = self.params.SIMULATION_LENGTH
    self.simulationLengthLabel.text = f'Simulation Length (10 - 500): {self.simulationLengthSlider.start}'
    
    self.gridSizeSlider.start = self.params.GRID_SIZE
    self.gridSizeLabel.text = f'Grid Size (1 - 10): {self.gridSizeSlider.start}'
    
    self.infectionRateSlider.start = round(self.params.INFECTION_RATE * 100)
    self.infectionRateLabel.text = f'Infection Rate (1 - 100): {self.infectionRateSlider.start}'
  
    self.incubationPeriodSlider.start = self.params.INCUBATION_PERIOD
    self.incubationPeriodLabel.text = f'Incubation Period (1 - 100): {self.incubationPeriodSlider.start}'
    
    self.infectionPeriodSlider.start = self.params.INFECTION_PERIOD
    self.infectionPeriodLabel.text = f'Infection Period (1 - 100): {self.infectionPeriodSlider.start}'
    
    self.immunityPeriodSlider.start = self.params.IMMUNITY_PERIOD
    self.immunityPeriodLabel.text = f'Immunity Period (1 - 100): {self.immunityPeriodSlider.start}'
    
    self.mortalityRateSlider.start = round(self.params.MORTALITY_RATE * 100)
    self.mortalityRateLabel.text = f'Mortality Rate (1 - 100): {self.mortalityRateSlider.start}'
    
    self.ruleComplianceRateSlider.start = round(self.params.RULE_COMPLIANCE_RATE * 100)
    self.ruleComplianceRateLabel.text = f'Rule Compliance Rate (0 - 100): {self.ruleComplianceRateSlider.start}'
    
    self.vaccinationSwitch.checked = self.params.VACCINATION_ENABLED
    self.vaccinationRateSlider.visible = self.params.VACCINATION_ENABLED
    self.vaccinationRateSlider.start = round(self.params.VACCINATION_RATE * 30 * 100)
    
    self.lockdownSwitch.checked = self.params.LOCKDOWN_ENABLED
    self.lockdownSlider.visible = self.params.LOCKDOWN_ENABLED
    self.lockdownSlider.start = round(self.params.LOCKDOWN_LEVEL * 100)
    
    self.hygieneSwitch.checked = self.params.HYGIENE_ENABLED
    
    self.travelSwitch.checked = self.params.TRAVEL_RESTRICTIONS_ENABLED
    
    self.hospitalCapacitySlider.start = round(self.params.HOSPITAL_CAPACITY * 100)
    self.hospitalCapacityLabel.text = f'Hospital Capacity (0 - 100): {self.hospitalCapacitySlider.start}'
    
  def onPopulationSizeChange(self, **event_args):
    '''This method is called when the population size slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.POPULATION_SIZE = self.populationSizeSlider.value
    self.populationSizeLabel.text = f'Population Size (10 - 1000): {self.populationSizeSlider.value}'
  
  def onPopulationDemographicsChange(self, handle, **event_args):
    '''This method is called when the population demographic sliders are moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    demographicsValues = self.populationSizeSlider.values
    self.params.POPULATION_DEMOGRAPHICS = [demographicsValues[0] / 100]
    self.params.POPULATION_DEMOGRAPHICS.append(1 - sum(self.params.POPULATION_DEMOGRAPHICS))
    self.populationDemographicsLabel.text = f'''Population Demographics: 
    0 - 15: {demographicsValues[0]}
    15 - 45: {demographicsValues[1] - demographicsValues[0]}
    45 - 65: {demographicsValues[2] - demographicsValues[1]}
    65+: {demographicsValues[3] - demographicsValues[2]}'''

  def onSimulationLengthChange(self, **event_args):
    '''This method is called when the simulation length slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''

    self.params.SIMULATION_LENGTH = self.simulationLengthSlider.value
    self.simulationLengthLabel.text = f'Simulation Length (10 - 500): {self.simulationLengthSlider.value}'
  
  def onGridSizeChange(self, handle, **event_args):
    '''This method is called when the grid size slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.GRID_SIZE = self.gridSizeSlider.value
    self.params.CELL_SIZE = 1 / self.params.GRID_SIZE
    self.gridSizeLabel.text = f'Grid Size (1 - 10): {self.gridSizeSlider.value}'

  def onInfectionRateChange(self, **event_args):
    '''This method is called when the infection rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''

    self.params.INFECTION_RATE = self.infectionRateSlider.value / 100
    self.infectionRateLabel.text = f'Infection Rate (1 - 100): {self.infectionRateSlider.value}'

  def onIncubationPeriodChange(self, **event_args):
    '''This method is called when the incubation period slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''

    self.params.INCUBATION_PERIOD = self.incubationPeriodSlider.value
    self.incubationPeriodLabel.text = f'Incubation Period (1 - 100): {self.incubationPeriodSlider.value}'

  def onInfectionPeriodChange(self, **event_args):
    '''This method is called when the infection period slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''

    self.params.INFECTION_PERIOD = self.infectionPeriodSlider.value
    self.infectionPeriodLabel.text = f'Infection Period (1 - 100): {self.infectionPeriodSlider.value}'
    
  def onImmunityPeriodChange(self, handle, **event_args):
    '''This method is called when the immunity period slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.IMMUNITY_PERIOD = self.immunityPeriodSlider.value
    self.immunityPeriodLabel.text = f'Immunity Period (1 - 100): {self.immunityPeriodSlider.value}'

  def onMortalityRateChange(self, **event_args):
    '''This method is called when the mortality rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.INFECTION_RATE = self.mortalityRateSlider.value / 100
    self.mortalityRateLabel.text = f'Mortality Rate (1 - 100): {self.mortalityRateSlider.value}'
    
  def onRuleComplianceRateChange(self, handle, **event_args):
    '''"This method is called when the rule compliance rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.RULE_COMPLIANCE_RATE = self.ruleComplianceRateSlider.value / 100
    self.ruleComplianceRateLabel.text = f'Rule Compliance Rate (0 - 100): {self.ruleComplianceRateSlider.value}'
    
  def onVaccinationChange(self, **event_args):
    '''This method is called when the vaccination switch is checked or unchecked
    
    Parameters
    ----------
    **event_args
      Details about how the switch is checked
    
    Returns
    -------
    None
    '''
    
    self.params.VACCINATION_ENABLED = self.vaccinationSwitch.checked
    self.vaccinationRateSlider.visible = self.params.VACCINATION_ENABLED
    if self.params.VACCINATION_ENABLED:
      self.vaccinationLabel.text = f'Vaccination Rate (5 - 50): {self.vaccinationRateSlider.value}'
    else:
      self.vaccinationLabel.text = 'Vaccination: '
    
  def onVaccinationRateChange(self, handle, **event_args):
    '''"This method is called when the vaccination rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.VACCINATION_RATE = self.vaccinationRateSlider.value / 30 / 100
    self.vaccinationLabel.text = f'Vaccination Rate (5 - 50): {self.vaccinationRateSlider.value}'

  def onLockdownChange(self, **event_args):
    '''This method is called when the lockdown switch is checked or unchecked
    
    Parameters
    ----------
    **event_args
      Details about how the switch is checked
    
    Returns
    -------
    None
    '''
    
    self.params.LOCKDOWN_ENABLED = self.lockdownSwitch.checked
    self.lockdownSlider.visible = self.params.LOCKDOWN_ENABLED
    if self.params.LOCKDOWN_ENABLED:
      self.lockdownLabel.text = f'Lockdown Level (0 - 100): {self.lockdownSlider.value}'
    else:
      self.lockdownLabel.text = 'Lockdown: '

  def onLockdownLevelChange(self, handle, **event_args):
    '''"This method is called when the lockdown rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.LOCKDOWN_LEVEL = self.lockdownSlider.value / 100
    self.lockdownLabel.text = f'Lockdown Rate (0 - 100): {self.lockdownSlider.value}'

  def onHygieneChange(self, **event_args):
    '''This method is called when the hygiene switch is checked or unchecked
    
    Parameters
    ----------
    **event_args
      Details about how the switch is checked
    
    Returns
    -------
    None
    '''
    
    self.params.HYGIENE_ENABLED = self.hygieneSwitch.checked

  def onHospitalityRateChange(self, handle, **event_args):
    '''This method is called when the hospital rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''

    self.params.HOSPITAL_CAPACITY = self.hospitalCapacitySlider.value / 100
    self.hospitalCapacityLabel.text = f'Hospital Capacity (0 - 100): {self.hospitalCapacitySlider.value}'
    

  def onTravelRestrictionsChange(self, **event_args):
    '''This method is called when the travel restrictions switch is checked or unchecked
    
    Parameters
    ----------
    **event_args
      Details about how the switch is checked
    
    Returns
    -------
    None
    '''
    
    self.params.TRAVEL_RESTRICTIONS_ENABLED = self.travelSwitch.checked
    