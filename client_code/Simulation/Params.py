import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from math import log

from Interventions import Interventions # type: ignore

class Params:
  '''Parameters for the simulation.
  
  Simulation Parameters
  ---------------------
  POPULATION_SIZE : int
    The size of the population in the simulation
  POPULATION_DEMOGRAPHICS
    The spread of population amongst different ages
  SIMULATION_LENGTH
    The number of frams in the simulation
  CONTACT_RADIUS : float
    The maximum distance between two individuals who are in contact
  CONTACT_RADIUS_SQUARED : float
    The square of the CONTACT_RADIUS for easier calculations
  TIME_PER_FRAME : float
    Time taken per frame
  GRID_SIZE : int
    The number of rows and columns of the grid
  GRID_PROBABILITIES : List[List[float]]
    The probability of a person landing in each cell
  CELL_SIZE : float
    The size of the side of each cell
  MAX_MOVEMENT : float
    The maximum distance a person can move in a direction
  TRAVEL_RATE : float
    The probability of a person travelling to another cell
  TRAVEL_PROBABILITES : List[List[List[List[float]]]]
    The list of probabilities of going from one cell to another cell
  RANDOM_SEED : int
    The seed for the random number generator used in the simulation
  
  Metrics Parameters
  ------------------
  DOUBLING_TIME_WINDOW_LENGTH : int
    The number of frames in the window used to calculate doubling time
  LOG_2 : float
    The log of 2
  PLOT_EFFECTIVE_REPRODUCTIVE_NUMBER : bool
    Whether to plot the effective reproductive number

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
  HOSPITALIZATION_RATE : float
    The percentage of the infected population that is hospitalised
  MORTALITY_COEFFICIENT : float
    The amount by which the mortality rate increases when the 
    hospitalized patients exceed hospital capacity
  INITIAL_INFECTED : int
    The number of people who are infected at the beginning
  
  Intervention Parameters
  -----------------------
  RULE_COMPLIANCE_RATE : float
    The percentage of the population that follows rules
  
  
  Hospital Parameters
  -------------------
  HOSPITAL_CAPACITY : float
    The percentage of the population that can be supported by hospitals
  HOSPITALIZATION_COST : int
    The cost of a person being in hospital per person per day
  HOSPITAL_ENABLED : bool
    Whether we are tracking hospital cases
  
  Vaccination Parameters
  ----------------------
  VACCINATION_ENABLED : bool
    Whether vaccination is enabled
  VACCINATION_START : bool
    The day vaccination starts
  VACCINATION_RATE : float
    The percentage of suseptible population which gets vaccinated in a day
  VACCINATION_COST : int
    The cost of one vaccination
  INITIAL_VACCINATED : int
    The number of people who are vaccinated at the begining

  Lockdown Parameters
  ---------------------
  LOCKDOWN_ENABLED : bool
    Whether lockdown is enabled
  LOCKDOWN_COST : int
    The cost of lockdown per person per day
  LOCKDOWN_DAYS : List[int]
    The days on which a global lockdown are enabled
  LOCAL_LOCKDOWN : bool
    Whether the lockdown is local or global
  LOCKDOWN_STRATEGY : func
    The strategy used for deciding which days are lockdown
  LOCKDOWN_STRATEGIES : Dict[str, func]
    Dictionary of all lockdown strategies
  
  Lockdown strategy Parameters
  ----------------------------
  LOCKDOWN_LEVEL : float
    The percentage of infected population at which lockdown is enabled
  LOCKDOWN_START : int
    When the lockdown strategy starts
  LOCKDOWN_STOP : int
    When the lockdown strategy stops
  ALT_LOCKDOWN_FRAMES_ON : int
    How long the lockdown is kept on for
  ALT_LOCKDOWN_FRAMES_OFF : int
    How long the lockdown is kept off for
  DAY_LOCKDOWN : List[bool]
    Which days of the week lockdown is enabled
  
  Hygiene measures Parameters
  ---------------------------
  HYGIENE_ENABLED : bool
    Whether hygiene measures are enabled
  HYGIENE_RATE : float
    Rate by which infection decreases when hygiene measures are enabled
  HYGIENE_COST : int
    Cost of implementing hygiene measures
  
  Travel Restrictions Parameters
  ------------------------------
  TRAVEL_RESTRICTIONS_ENABLED : bool
    Whether travel restrictions are enabled
  TRAVEL_RESTRICTIONS_COST : int
    Cost of travel restrictions per person who doesnt travel per day
  '''
  
  # Set lockdown strategies
  LOCKDOWN_STRATEGIES = {
    'alternating': Interventions.alternatingLockdown,
    'days-of-the-week': Interventions.daysOfWeekLockdown,
    'block': Interventions.blockLockdown
  }
  
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
    self.POPULATION_SIZE = 2500
    self.POPULATION_DEMOGRAPHICS = [0.35, 0.8, 0.95, 1]
    self.SIMULATION_LENGTH = 180
    self.TIME_PER_FRAME = 0.2
    self.GRID_SIZE = 3
    self.CELL_SIZE = 1 / self.GRID_SIZE
    self.MAX_MOVEMENT = 0.05
    self.TRAVEL_RATE = 0.1
    self.COMORBIDITY_COEFFICIENTS = [0.7, 0.9, 1.1, 1.3]
    self.RANDOM_SEED = 0
    self.GRID_PROBABILITIES = [0.1312769922816259, 0.1390833168942316, 0.3045853365542704, 0.4356598378729931, 0.5622315487782497, 0.661694550602876, 0.7233137507793976, 0.9097747150485921, 1.0]
    self.TRAVEL_PROBABILITES = [[[0.0, 0.10929820017699199, 0.27276162832436446, 0.3757530039414913, 0.4070611554404322, 0.5141784494471481, 0.6862885066982833, 0.8897540885298117, 1.0], [0.01276555432675935, 0.01276555432675935, 0.2549058943340527, 0.3165936951304174, 0.3313424092336104, 0.5261744388243516, 0.605427611942261, 0.8333672107397323, 1.0], [0.15892428359862334, 0.25671979924004384, 0.25671979924004384, 0.4112738227241321, 0.4689758058768651, 0.5133234764625129, 0.6529014952735729, 0.9486386571496084, 1.0]], [[0.10971379925019822, 0.2878653035220132, 0.32803681379718236, 0.32803681379718236, 0.41482954573864717, 0.5309870905775683, 0.6608006095631672, 0.75172681155559, 1.0], [0.009644405249296112, 0.2094320374511056, 0.4376333030633881, 0.45569664963375833, 0.45569664963375833, 0.7076895066463159, 0.8330073254559883, 0.901153496212128, 1.0], [0.06026892867591995, 0.19565788907547954, 0.32939093982734113, 0.5182163362815277, 0.6682045420575002, 0.6682045420575002, 0.8840014633111152, 0.9638518606813694, 1.0]], [[0.08414150309199522, 0.18637911894866807, 0.24348125544191232, 0.4330323728765049, 0.5914437868519774, 0.7308537039886345, 0.7308537039886345, 0.8950430045152277, 1.0], [0.19785810173842416, 0.2650401869246098, 0.319379404747021, 0.4786510388002174, 0.6844413299933607, 0.7661163638941053, 0.8477272086754665, 0.8477272086754665, 1.0], [0.2126451818934487, 0.26513495503947604, 0.3493490329508198, 0.6236939408914254, 0.6542097654894706, 0.688875326780259, 0.7852000076475122, 1.0, 1.0]]]
    
    # Contact radius
    # The contact radius is a function of the population density
    # CONTACT_RADIUS = 3 / POPULATION_DENSITY
    self.CONTACT_RADIUS = 3 / self.POPULATION_SIZE
    self.CONTACT_RADIUS_SQUARED = self.CONTACT_RADIUS ** 2

    # State transition related parameters
    self.INITIAL_INFECTED = 2
    self.INFECTION_RATE = 0.2
    self.HOSPITALIZATION_RATE = 0.5
    self.MORTALITY_RATE = 0.2 * self.HOSPITALIZATION_RATE
    self.MORTALITY_COEFFICIENT = 2
    self.INCUBATION_PERIOD = 5
    self.INFECTION_PERIOD = 10
    self.IMMUNITY_PERIOD = 30
    
    # Metrics related parameters
    self.DOUBLING_TIME_WINDOW_LENGTH = 3
    self.LOG_2 = log(2)
    self.PLOT_EFFECTIVE_REPRODUCTIVE_NUMBER = False

    # Intervention related parameters
    self.RULE_COMPLIANCE_RATE = 0.9

    # Hospital related paramters
    self.HOSPITAL_CAPACITY = 0.06
    self.HOSPITALIZATION_COST = 5000
    self.HOSPITAL_ENABLED = False

    # Vaccination related parameters
    self.VACCINATION_ENABLED = False
    self.VACCINATION_START = 60
    self.VACCINATION_RATE = 0.01
    self.VACCINATION_COST = 1000
    self.INITIAL_VACCINATED = 0

    # Lockdown related parameters
    self.LOCKDOWN_ENABLED = False
    self.LOCKDOWN_COST = 500
    self.LOCKDOWN_DAYS = []
    self.LOCAL_LOCKDOWN = False
    self.LOCKDOWN_STRATEGY = 'block'
    
    # Lockdown strategy related parameters
    self.LOCKDOWN_LEVEL = 0.5
    self.LOCKDOWN_START = 50
    self.LOCKDOWN_STOP = 100
    self.ALT_LOCKDOWN_FRAMES_ON = 20
    self.ALT_LOCKDOWN_FRAMES_OFF = 10
    self.DAY_LOCKDOWN = [True, True, True, True, True, False, False]

    # Hygiene related parameters
    self.HYGIENE_ENABLED = False
    self.HYGIENE_RATE = 0.6
    self.HYGIENE_COST = 100

    # Travel restrictions related parameters
    self.TRAVEL_RESTRICTIONS_ENABLED = False
    self.TRAVEL_RESTRICTIONS_COST = 200

    # Change the value for each parameter in kwargs from default
    for param, value in kwargs.items():
      setattr(self, str(param), value)
