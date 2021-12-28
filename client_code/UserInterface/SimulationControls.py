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
    
    # Population parameters UI initialization
    self.populationSizeSlider.start = self.params.POPULATION_SIZE
    self.populationSizeLabel.text = f'Population Size: {self.populationSizeSlider.start} people'
    demographicsStart = [round(i * 100) for i in self.params.POPULATION_DEMOGRAPHICS]
    self.populationDemographicsSlider.start = demographicsStart
    self.populationDemographicsLabel.text = f'''Population Demographics: 
    0 - 15: {demographicsStart[0]}%
    15 - 45: {demographicsStart[1] - demographicsStart[0]}%
    45 - 65: {demographicsStart[2] - demographicsStart[1]}%
    65+: {demographicsStart[3] - demographicsStart[2]}%'''
    
    # Simulation length UI initialization
    self.simulationLengthSlider.start = self.params.SIMULATION_LENGTH
    self.simulationLengthLabel.text = f'Simulation Length: {self.simulationLengthSlider.start} days'
    
    # Grid size UI initialization
    self.gridSizeSlider.start = self.params.GRID_SIZE
    self.gridSizeLabel.text = f'Grid Size: {self.gridSizeSlider.start}'
    
    # Infection rate UI initialization
    self.infectionRateSlider.start = round(self.params.INFECTION_RATE * 100)
    self.infectionRateLabel.text = f'Infection Probability: {self.infectionRateSlider.start}%'
    
    # Disease timeline parameters UI initialization
    self.diseaseTimelineSlider.max = self.simulationLengthSlider.start
    self.diseaseTimelineSlider.start = [
      self.params.INCUBATION_PERIOD,
      self.params.INCUBATION_PERIOD + self.params.INFECTION_PERIOD,
      self.params.INCUBATION_PERIOD + self.params.INFECTION_PERIOD + self.params.IMMUNITY_PERIOD
    ]
    self.diseaseTimelineLabel.text = f'''Disease Timeline: 
    Incubation Period: {self.params.INCUBATION_PERIOD} days
    Infection Period: {self.params.INFECTION_PERIOD} days
    Immunity Period: {self.params.IMMUNITY_PERIOD} days'''
    
    # Morality rate UI initialization
    self.mortalityRateSlider.start = round(self.params.MORTALITY_RATE * 100)
    self.mortalityRateLabel.text = f'Mortality Probability: {self.mortalityRateSlider.start}%'
    
    # Rule compliance rate UI initialization
    self.ruleComplianceRateSlider.start = round(self.params.RULE_COMPLIANCE_RATE * 100)
    self.ruleComplianceRateLabel.text = f'Rule Compliance Probability: {self.ruleComplianceRateSlider.start}%'
    
    # Vaccination UI initialization
    self.vaccinationSwitch.checked = self.params.VACCINATION_ENABLED
    self.vaccinationRateSlider.visible = self.params.VACCINATION_ENABLED
    self.vaccinationRateSlider.start = round(self.params.VACCINATION_RATE * 30 * 100)
    self.vaccinationCostSlider.visible = self.params.VACCINATION_ENABLED
    self.vaccinationCostSlider.start = self.params.VACCINATION_COST
    
    # Lockdown UI initialization
    self.lockdownSwitch.checked = self.params.LOCKDOWN_ENABLED
    self.lockdownSlider.visible = self.params.LOCKDOWN_ENABLED
    self.lockdownSlider.start = round(self.params.LOCKDOWN_LEVEL * 100)
    self.lockdownCostSlider.visible = self.params.LOCKDOWN_ENABLED
    self.lockdownCostSlider.start = self.params.LOCKDOWN_COST
    
    # Hygiene UI initialization
    self.hygieneSwitch.checked = self.params.HYGIENE_ENABLED
    self.hygieneCostSlider.visible = self.params.HYGIENE_ENABLED
    self.hygieneCostSlider.start = self.params.HYGIENE_COST
    
    # Travel UI initialization
    self.travelSwitch.checked = self.params.TRAVEL_RESTRICTIONS_ENABLED
    self.travelRestrictionsCostSlider.visible = self.params.TRAVEL_RESTRICTIONS_ENABLED
    self.travelRestrictionsCostSlider.start = self.params.TRAVEL_RESTRICTIONS_COST
    
    # Hospital parameters UI initialization
    self.hospitalCapacitySlider.start = round(self.params.HOSPITAL_CAPACITY * 100)
    self.hospitalizationCostSlider.start = self.params.HOSPITALIZATION_COST
    self.hospitalCapacityLabel.text = f'Hospital Capacity: {self.hospitalCapacitySlider.start}%, Cost: Rs. {self.hospitalizationCostSlider.start}'
    
  def onPopulationSizeChange(self, **event_args):
    '''This method is called when the population size slider is moved'''
    
    self.params.POPULATION_SIZE = int(round(self.populationSizeSlider.value))
    self.params.HOSPITAL_CAPACITY = 0.2
    self.populationSizeLabel.text = f'Population Size: {int(round(self.populationSizeSlider.value))} people'
  
  def onPopulationDemographicsChange(self, handle, **event_args):
    '''This method is called when the population demographic sliders are moved'''
    
    demographicsValues = [int(round(i)) for i in self.populationDemographicsSlider.values]
    self.params.POPULATION_DEMOGRAPHICS = [demographicsValues[0] / 100]
    self.params.POPULATION_DEMOGRAPHICS.append(1 - sum(self.params.POPULATION_DEMOGRAPHICS))
    self.populationDemographicsLabel.text = f'''Population Demographics: 
    0 - 15: {demographicsValues[0]}%
    15 - 45: {demographicsValues[1] - demographicsValues[0]}%
    45 - 65: {demographicsValues[2] - demographicsValues[1]}%
    65+: {100 - demographicsValues[2]}%'''

  def onSimulationLengthChange(self, **event_args):
    '''This method is called when the simulation length slider is moved'''

    self.params.SIMULATION_LENGTH = int(round(self.simulationLengthSlider.value))
    self.diseaseTimelineSlider.max = self.params.SIMULATION_LENGTH
    self.simulationLengthLabel.text = f'Simulation Length: {int(round(self.simulationLengthSlider.value))} days'
  
  def onGridSizeChange(self, handle, **event_args):
    '''This method is called when the grid size slider is moved'''
    
    self.params.GRID_SIZE = int(round(self.gridSizeSlider.value))
    self.params.CELL_SIZE = 1 / self.params.GRID_SIZE
    self.gridSizeLabel.text = f'Grid Size: {int(round(self.gridSizeSlider.value))}'

  def onInfectionRateChange(self, **event_args):
    '''This method is called when the infection rate slider is moved'''

    self.params.INFECTION_RATE = self.infectionRateSlider.value / 100
    self.infectionRateLabel.text = f'Infection Probability: {int(round(self.infectionRateSlider.value))}%'
    
  def onDiseaseTimelineChange(self, **event_args):
    '''This method is called when the disease timline sliders are moved'''
    
    timeline = [int(round(i)) for i in self.diseaseTimelineSlider.values]
    self.params.INCUBATION_PERIOD = max(1, timeline[0])
    self.params.INFECTION_PERIOD = max(1, timeline[1] - timeline[0])
    self.params.IMMUNITY_PERIOD = max(1, timeline[2] - timeline[1])
    self.diseaseTimelineLabel.text = f'''Disease Timeline: 
    Incubation Period: {int(round(self.params.INCUBATION_PERIOD))} days
    Infection Period: {int(round(self.params.INFECTION_PERIOD))} days
    Immunity Period: {int(round(self.params.IMMUNITY_PERIOD))} days'''
  
  def onMortalityRateChange(self, **event_args):
    '''This method is called when the mortality rate slider is moved'''
    
    self.params.MORTALITY_RATE = self.mortalityRateSlider.value / 100
    self.params.HOSPITALIZATION_RATE = 5 * self.params.MORTALITY_RATE
    self.mortalityRateLabel.text = f'Mortality Probability: {int(round(self.mortalityRateSlider.value))}%'
    
  def onRuleComplianceRateChange(self, handle, **event_args):
    '''This method is called when the rule compliance rate slider is moved'''
    
    self.params.RULE_COMPLIANCE_RATE = self.ruleComplianceRateSlider.value / 100
    self.ruleComplianceRateLabel.text = f'Rule Compliance Probability: {int(round(self.ruleComplianceRateSlider.value))}%'
    
  def onVaccinationChange(self, **event_args):
    '''This method is called when the vaccination switch is checked or unchecked'''
    
    self.params.VACCINATION_ENABLED = self.vaccinationSwitch.checked
    self.vaccinationRateSlider.visible = self.params.VACCINATION_ENABLED
    self.vaccinationCostSlider.visible = self.params.VACCINATION_ENABLED
    if self.params.VACCINATION_ENABLED:
      self.vaccinationLabel.text = f'Vaccination Rate: {self.vaccinationRateSlider.value}%, Cost: Rs. {self.vaccinationCostSlider.value}'
    else:
      self.vaccinationLabel.text = 'Vaccination: '
    
  def onVaccinationRateChange(self, handle, **event_args):
    '''"This method is called when the vaccination rate slider is moved'''
    
    self.params.VACCINATION_RATE = self.vaccinationRateSlider.value / 30 / 100
    self.vaccinationLabel.text = f'Vaccination Rate: {int(round(self.vaccinationRateSlider.value))}%, Cost: Rs. {int(round(self.vaccinationCostSlider.value))}'
    
  def onVaccinationCostChange(self, handle, **event_args):
    '''"This method is called when the vaccination cost slider is moved'''
    
    self.params.VACCINATION_COST = int(round(self.vaccinationCostSlider.value))
    self.vaccinationLabel.text = f'Vaccination Rate: {int(round(self.vaccinationRateSlider.value))}%, Cost: Rs. {int(round(self.vaccinationCostSlider.value))}'

  def onLockdownChange(self, **event_args):
    '''This method is called when the lockdown switch is checked or unchecked'''
    
    self.params.LOCKDOWN_ENABLED = self.lockdownSwitch.checked
    self.lockdownSlider.visible = self.params.LOCKDOWN_ENABLED
    self.lockdownCostSlider.visible = self.params.LOCKDOWN_ENABLED
    if self.params.LOCKDOWN_ENABLED:
      self.lockdownLabel.text = f'Lockdown Level: {self.lockdownSlider.value}%, Cost: Rs. {self.lockdownCostSlider.value}'
    else:
      self.lockdownLabel.text = 'Lockdown: '

  def onLockdownLevelChange(self, handle, **event_args):
    '''This method is called when the lockdown level slider is moved'''
    
    self.params.LOCKDOWN_LEVEL = self.lockdownSlider.value / 100
    self.lockdownLabel.text = f'Lockdown Level: {int(round(self.lockdownSlider.value))}%, Cost: Rs. {int(round(self.lockdownCostSlider.value))}'
  
  def onLockdownCostChange(self, handle, **event_args):
    '''This method is called when the lockdown cost slider is moved'''

    self.params.LOCKDOWN_COST = int(round(self.lockdownCostSlider.value))
    self.lockdownLabel.text = f'Lockdown Level: {int(round(self.lockdownSlider.value))}%, Cost: Rs. {int(round(self.lockdownCostSlider.value))}'

  def onHygieneChange(self, **event_args):
    '''This method is called when the hygiene switch is checked or unchecked'''

    self.params.HYGIENE_ENABLED = self.hygieneSwitch.checked
    self.hygieneCostSlider.visible = self.params.HYGIENE_ENABLED
    if self.params.HYGIENE_ENABLED:
      self.hygieneLabel.text = f'Hygiene Measures Cost: Rs. {self.hygieneCostSlider.value}'
    else:
      self.hygieneLabel.text = 'Hygiene Measures: '
  
  def onHygieneCostChange(self, handle, **event_args):
    '''This method is called when the hygiene cost slider is moved'''
    
    self.params.HYGIENE_COST = int(round(self.hygieneCostSlider.value))
    self.hygieneLabel.text = f'Hygiene Measures Cost: Rs. {int(round(self.hygieneCostSlider.value))}'

  def onHospitalityRateChange(self, handle, **event_args):
    '''This method is called when the hospital rate slider is moved'''

    self.params.HOSPITAL_CAPACITY = self.hospitalCapacitySlider.value / 100
    self.hospitalCapacityLabel.text = f'Hospital Capacity: {int(round(self.hospitalCapacitySlider.value))}%, Cost: Rs. {int(round(self.hospitalizationCostSlider.value))}'
    
  def onHospitalizationCostChange(self, handle, **event_args):
    '''This method is called when the hospitalization cost slider is moved'''
    
    self.params.HOSPITALIZATION_COST = int(round(self.hospitalizationCostSlider.value))
    self.hospitalCapacityLabel.text = f'Hospital Capacity: {int(round(self.hospitalCapacitySlider.value))}%, Cost: Rs. {int(round(self.hospitalizationCostSlider.value))}'

  def onTravelRestrictionsChange(self, **event_args):
    '''This method is called when the travel restrictions switch is checked or unchecked'''
    
    self.params.TRAVEL_RESTRICTIONS_ENABLED = self.travelSwitch.checked
    self.travelRestrictionsCostSlider.visible = self.params.TRAVEL_RESTRICTIONS_ENABLED
    if self.params.TRAVEL_RESTRICTIONS_ENABLED:
      self.travelLabel.text = f'Travel Restrictions Cost: Rs. {self.travelRestrictionsCostSlider.value}'
    else:
      self.travelLabel.text = 'Travel Restrictions: : '
  
  def onTravelRestrictionsCostChange(self, handle, **event_args):
    '''This method is called when the travel restrictions cost slider is moved'''
    
    self.params.TRAVEL_RESTRICTIONS_COST = int(round(self.travelRestrictionsCostSlider.value))
    self.travelLabel.text = f'Travel Restrictions Cost: Rs. {int(round(self.travelRestrictionsCostSlider.value))}'
