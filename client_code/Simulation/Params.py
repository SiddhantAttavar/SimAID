import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Params:
  '''Parameters for the simulation.
  
  Simulation Parameters
  ---------------------
  POPULATION_SIZE
    The size of the population in the simulation
  POPULATION_DEMOGRAPHICS
    The spread of population amongst different ages
  SIMULATION_LENGTH
    The number of frams in the simulation
  CONTACT_RADIUS : float
    The maximum distance between two individuals who are in contact
  TIME_PER_FRAME : float
    Time taken per frame
  GRID_SIZE : int
    The number of rows and columns of the grid
  GRID_PROBABILITIES : list(list(float))
    The probability of a person landing in each cell
  CELL_SIZE : float
    The size of the side of each cell
  MAX_MOVEMENT : float
    The maximum distance a person can move in a direction
  TRAVEL_RATE : float
    The probability of a person travelling to another cell
  TRAVEL_PROBABILITES : list(list(list(list(float))))
    The list of probabilities of going from one cell to another cell
  
  Pathogen Parameters
  -------------------
  INFECTION_RATE : float
    The chance of an infected person infecting a suseptible person
  INCUBATION_PERIOD : int
    The duration for which an infected person is asymptomatic
  INFECTION_PERIOD : int
    The duration for which an infected person has the disease
  MORTALITY_RATE : float
    The chance of an infected person dying
  INITIAL_INFECTED : int
    The number of people who are infected at the beginning
  
  Intervention Parameters
  -----------------------
  RULE_COMPLIANCE_RATE : float
    The percentage of the population that follows rules
  HOSPITALITY_CAPACITY : float
    The percentage of the population that can be supported by hospitals
  
  Vaccination Parameters
  ----------------------
  VACCINATION_ENABLED : bool
    Whether vaccination is enabled
  VACCINATION_RATE : float
    The percentage of suseptible population which gets vaccinated in a day

  Lockdown Parameters
  ---------------------
  LOCKDOWN_ENABLED : bool
    Whether lockdown is enabled
  LOCKDOWN_LEVEL : float
    The percentage of infected population at which lockdown is enabled
  
  Hygiene measures Parameters
  ---------------------------
  HYGIENE_ENABLED : bool
    Whether hygiene measures are enabled
  HYGIENE_RATE : float
    Rate by which infection decreases when hygiene measures are enabled
  
  Travel Restrictions Parameters
  ------------------------------
  TRAVEL_RESTRICTIONS_ENABLED : bool
    Whether travel restrictions are enabled
  '''

  def __init__(self, **kwargs):
    '''Initializes the parameters.

    Parameters
    ----------
    **kwargs
      Arguments to change the default parameters
    
    Returns
    -------
    None
    '''

    # Basic model related parameters
    self.POPULATION_SIZE = 300
    self.POPULATION_DEMOGRAPHICS = [0.35, 0.8, 0.95, 1]
    self.SIMULATION_LENGTH = 50
    self.CONTACT_RADIUS = 0.1
    self.TIME_PER_FRAME = 0.5
    self.GRID_SIZE = 3
    self.GRID_PROBABILITIES = []
    self.CELL_SIZE = 1 / self.GRID_SIZE
    self.MAX_MOVEMENT = 0.05
    self.TRAVEL_RATE = 0.4
    self.TRAVEL_PROBABILITES = []
    self.COMORBIDITY_COEFFICIENTS = [0.5, 0.7, 0.9, 1]

    # Intervention related parameters
    self.RULE_COMPLIANCE_RATE = 0.9
    self.HOSPITAL_CAPACITY = 0.3

    # State transition related parameters
    self.INITIAL_INFECTED = 2
    self.INFECTION_RATE = 0.6
    self.INCUBATION_PERIOD = 3
    self.INFECTION_PERIOD = 10
    self.MORTALITY_RATE = 0.3
    self.IMMUNITY_PERIOD = 30

    # Vaccination related parameters
    self.VACCINATION_ENABLED = False
    self.VACCINATION_RATE = 0.01

    # Lockdown related parameters
    self.LOCKDOWN_ENABLED = False
    self.LOCKDOWN_LEVEL = 0.5

    # Hygiene related parameters
    self.HYGIENE_ENABLED = False
    self.HYGIENE_RATE = 0.6

    # Travel restrictions related parameters
    self.TRAVEL_RESTRICTIONS_ENABLED = False

    # Change the value for each parameter in kwargs from default
    for param, value in kwargs.items():
      exec(f'self.{param} = {value}')