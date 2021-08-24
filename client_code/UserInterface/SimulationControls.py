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
    self.populationSizeLabel.text = f'Population Size: {self.populationSizeSlider.start} people'
    
    demographicsStart = [round(i * 100) for i in self.params.POPULATION_DEMOGRAPHICS]
    self.populationDemographicsSlider.start = demographicsStart
    self.populationDemographicsSlider.connect = [True, False, True, False]
    self.populationDemographicsLabel.text = f'''Population Demographics: 
    0 - 15: {demographicsStart[0]}%
    15 - 45: {demographicsStart[1] - demographicsStart[0]}%
    45 - 65: {demographicsStart[2] - demographicsStart[1]}%
    65+: {demographicsStart[3] - demographicsStart[2]}%'''
    
    self.simulationLengthSlider.start = self.params.SIMULATION_LENGTH
    self.simulationLengthLabel.text = f'Simulation Length: {self.simulationLengthSlider.start} days'
    
    self.gridSizeSlider.start = self.params.GRID_SIZE
    self.gridSizeLabel.text = f'Grid Size: {self.gridSizeSlider.start}'
    
    self.infectionRateSlider.start = round(self.params.INFECTION_RATE * 100)
    self.infectionRateLabel.text = f'Infection Rate: {self.infectionRateSlider.start}%'
  
    self.incubationPeriodSlider.start = self.params.INCUBATION_PERIOD
    self.incubationPeriodLabel.text = f'Incubation Period: {self.incubationPeriodSlider.start} days'
    
    self.infectionPeriodSlider.start = self.params.INFECTION_PERIOD
    self.infectionPeriodLabel.text = f'Infection Period: {self.infectionPeriodSlider.start} days'
    
    self.immunityPeriodSlider.start = self.params.IMMUNITY_PERIOD
    self.immunityPeriodLabel.text = f'Immunity Period: {self.immunityPeriodSlider.start} days'
    
    self.mortalityRateSlider.start = round(self.params.MORTALITY_RATE * 100)
    self.mortalityRateLabel.text = f'Mortality Rate: {self.mortalityRateSlider.start}%'
    
    self.ruleComplianceRateSlider.start = round(self.params.RULE_COMPLIANCE_RATE * 100)
    self.ruleComplianceRateLabel.text = f'Rule Compliance Rate: {self.ruleComplianceRateSlider.start}%'
    
    self.vaccinationSwitch.checked = self.params.VACCINATION_ENABLED
    self.vaccinationRateSlider.visible = self.params.VACCINATION_ENABLED
    self.vaccinationRateSlider.start = round(self.params.VACCINATION_RATE * 30 * 100)
    self.vaccinationCostSlider.visible = self.params.VACCINATION_ENABLED
    self.vaccinationCostSlider.start = self.params.VACCINATION_COST
    
    self.lockdownSwitch.checked = self.params.LOCKDOWN_ENABLED
    self.lockdownSlider.visible = self.params.LOCKDOWN_ENABLED
    self.lockdownSlider.start = round(self.params.LOCKDOWN_LEVEL * 100)
    self.lockdownCostSlider.visible = self.params.LOCKDOWN_ENABLED
    self.lockdownCostSlider.start = self.params.LOCKDOWN_COST
    
    self.hygieneSwitch.checked = self.params.HYGIENE_ENABLED
    self.hygieneCostSlider.visible = self.params.HYGIENE_ENABLED
    self.hygieneCostSlider.start = self.params.HYGIENE_COST
    
    self.travelSwitch.checked = self.params.TRAVEL_RESTRICTIONS_ENABLED
    self.travelRestrictionsCostSlider.visible = self.params.TRAVEL_RESTRICTIONS_ENABLED
    self.travelRestrictionsCostSlider.start = self.params.TRAVEL_RESTRICTIONS_COST
    
    self.hospitalCapacitySlider.start = round(self.params.HOSPITAL_CAPACITY * 100)
    self.hospitalizationCostSlider.start = self.params.HOSPITALIZATION_COST
    self.hospitalCapacityLabel.text = f'Hospital Capacity: {self.hospitalCapacitySlider.start}%, Cost: ₹{self.hospitalizationCostSlider.start}'
    
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
    self.populationSizeLabel.text = f'Population Size: {self.populationSizeSlider.value} people'
  
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
    
    demographicsValues = self.populationDemographicsSlider.values
    self.params.POPULATION_DEMOGRAPHICS = [demographicsValues[0] / 100]
    self.params.POPULATION_DEMOGRAPHICS.append(1 - sum(self.params.POPULATION_DEMOGRAPHICS))
    self.populationDemographicsLabel.text = f'''Population Demographics: 
    0 - 15: {demographicsValues[0]}%
    15 - 45: {demographicsValues[1] - demographicsValues[0]}%
    45 - 65: {demographicsValues[2] - demographicsValues[1]}%
    65+: {100 - demographicsValues[2]}%'''

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
    self.simulationLengthLabel.text = f'Simulation Length: {self.simulationLengthSlider.value} days'
  
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
    self.gridSizeLabel.text = f'Grid Size: {self.gridSizeSlider.value}'

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
    self.infectionRateLabel.text = f'Infection Rate: {self.infectionRateSlider.value}%'

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
    self.incubationPeriodLabel.text = f'Incubation Period: {self.incubationPeriodSlider.value} days'

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
    self.infectionPeriodLabel.text = f'Infection Period: {self.infectionPeriodSlider.value} days'
    
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
    self.immunityPeriodLabel.text = f'Immunity Period: {self.immunityPeriodSlider.value} days'

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
    self.mortalityRateLabel.text = f'Mortality Rate: {self.mortalityRateSlider.value}%'
    
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
    self.ruleComplianceRateLabel.text = f'Rule Compliance Rate: {self.ruleComplianceRateSlider.value}%'
    
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
    self.vaccinationCostSlider.visible = self.params.VACCINATION_ENABLED
    if self.params.VACCINATION_ENABLED:
      self.vaccinationLabel.text = f'Vaccination Rate: {self.vaccinationRateSlider.value}%, Cost: ₹{self.vaccinationCostSlider.value}'
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
    self.vaccinationLabel.text = f'Vaccination Rate: {self.vaccinationRateSlider.value}%, Cost: ₹{self.vaccinationCostSlider.value}'
    
  def onVaccinationCostChange(self, handle, **event_args):
    '''"This method is called when the vaccination cost slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.VACCINATION_COST = self.vaccinationCostSlider.value
    self.vaccinationLabel.text = f'Vaccination Rate: {self.vaccinationRateSlider.value}%, Cost: ₹{self.vaccinationCostSlider.value}'

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
    self.lockdownCostSlider.visible = self.params.LOCKDOWN_ENABLED
    if self.params.LOCKDOWN_ENABLED:
      self.lockdownLabel.text = f'Lockdown Level: {self.lockdownSlider.value}%, Cost: ₹{self.lockdownCostSlider.value}'
    else:
      self.lockdownLabel.text = 'Lockdown: '

  def onLockdownLevelChange(self, handle, **event_args):
    '''This method is called when the lockdown rate slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.LOCKDOWN_LEVEL = self.lockdownSlider.value / 100
    self.lockdownLabel.text = f'Lockdown Level: {self.lockdownSlider.value}%, Cost: ₹{self.lockdownCostSlider.value}'
  
  def onLockdownCostChange(self, handle, **event_args):
    '''This method is called when the lockdown cost slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.LOCKDOWN_COST = self.lockdownCostSlider.value
    self.lockdownLabel.text = f'Lockdown Level: {self.lockdownSlider.value}%, Cost: ₹{self.lockdownCostSlider.value}'

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
    self.hygieneCostSlider.visible = self.params.HYGIENE_ENABLED
    if self.params.HYGIENE_ENABLED:
      self.hygieneLabel.text = f'Hygiene Measures Cost: ₹{self.hygieneCostSlider.value}'
    else:
      self.hygieneLabel.text = 'Hygiene Measures: '
  
  def onHygieneCostChange(self, handle, **event_args):
    '''This method is called when the hygiene cost slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.HYGIENE_COST = self.hygieneCostSlider.value
    self.hygieneLabel.text = f'Hygiene Measures Cost: ₹{self.hygieneCostSlider.value}'

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
    self.hospitalCapacityLabel.text = f'Hospital Capacity: {self.hospitalCapacitySlider.value}%, Cost: ₹{self.hospitalizationCostSlider.value}'
    
  def onHospitalizationCostChange(self, handle, **event_args):
    '''This method is called when the hospitalization cost slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.HOSPITALIZATION_COST = self.hospitalizationCostSlider.value
    self.hospitalCapacityLabel.text = f'Hospital Capacity: {self.hospitalCapacitySlider.value}%, Cost: ₹{self.hospitalizationCostSlider.value}'

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
    self.travelRestrictionsCostSlider.visible = self.params.TRAVEL_RESTRICTIONS_ENABLED
    if self.params.TRAVEL_RESTRICTIONS_ENABLED:
      self.travelLabel.text = f'Travel Restrictions Cost: ₹{self.travelRestrictionsCostSlider.value}'
    else:
      self.travelLabel.text = 'Travel Restrictions: : '
  
  def onTravelRestrictionsCostChange(self, handle, **event_args):
    '''This method is called when the travel restrictions cost slider is moved
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''
    
    self.params.TRAVEL_RESTRICTIONS_COST = self.travelRestrictionsCostSlider.value
    self.travelLabel.text = f'Travel Restrictions Cost: ₹{self.travelRestrictionsCostSlider.value}'
