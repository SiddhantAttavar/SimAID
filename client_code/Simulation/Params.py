class Params:
  """Parameters for the simulation.
  
  Simulation Parameters
  ---------------------
  POPULATION_SIZE
    The size of the population in the simulation
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
  
  Vaccination Parameters
  ----------------------
  VACCINATION_ENABLED : bool
    Whether vaccination is enabled
  VACCINATION_RATE : float
    The percentage of suseptible population which gets vaccinated in a day
  
  Social distancing Parameters
  ----------------------------
  SOCIAL_DISTANCING_ENABLED : bool
    Whether social distancing is enabled
  SOCIAL_DISTANCING_MAX_MOVEMENT : float
    The percentage by which movement is reduced

  QUARANTINE Parameters
  ---------------------
  QUARANTINE_ENABLED : bool
    Whether quarantine is enabled
  QUARANTINE_SIZE : float
    Size of the side of the quarantine area
  QUARANTINE_RATE : float
    The percentage of infected population which is quarantined
  
  Hygiene measures Parameters
  ---------------------------
  HYGIENE_ENABLED : bool
    Whether hygiene measures are enabled
  """

  # Basic model related parameters
  POPULATION_SIZE = 100
  SIMULATION_LENGTH = 50
  CONTACT_RADIUS = 0.1
  TIME_PER_FRAME = 0.5
  GRID_SIZE = 5
  GRID_PROBABILITIES = []
  CELL_SIZE = 1 / GRID_SIZE
  MAX_MOVEMENT = 0.05

  # Person related parameters
  RULE_COMPLIANCE_RATE = 0.9

  # State transition related parameters
  INITIAL_INFECTED = 2
  INFECTION_RATE = 0.6
  INCUBATION_PERIOD = 3
  INFECTION_PERIOD = 10
  MORTALITY_RATE = 0.3

  # Vaccination related parameters
  VACCINATION_ENABLED = False
  VACCINATION_RATE = 0.01

  # Social distancing related parameters
  SOCIAL_DISTANCING_ENABLED = False
  SOCIAL_DISTANCING_MAX_MOVEMENT = 0.3 * MAX_MOVEMENT

  # Quarantine related parameters
  QUARANTINE_ENABLED = False
  QUARANTINE_SIZE = 1 / 3
  QUARANTINE_RATE = 0.5

  # Hygiene related parameters
  HYGIENE_ENABLED = False
  HYGIENE_RATE = 0.6

  def __init__(self, **kwargs):
    """Initializes the parameters.

    Parameters
    ----------
    **kwargs
      Arguments to change the default parameters
    
    Returns
    -------
    None
    """

    # Change the value for each parameter in kwargs from default
    for param, value in kwargs.items():
      exec(f'self.{param} = {value}')