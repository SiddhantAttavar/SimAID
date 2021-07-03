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
  MAX_MOVEMENT : float
    The maximum distance a person can move in a direction
  TIME_PER_FRAME : float
    Time taken per frame
  """

  # Basic model related parameters
  POPULATION_SIZE = 100
  SIMULATION_LENGTH = 50
  CONTACT_RADIUS = 0.1
  MAX_MOVEMENT = 0.05
  TIME_PER_FRAME = 0.2

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
  QUARANTINE_RATE = 0.8

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