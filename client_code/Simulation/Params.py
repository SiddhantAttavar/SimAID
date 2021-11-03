import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

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
  HOSPITALIZATION_RATE : float
    The percentage of the infected population that is hospitalised
  HOSPITALIZATION_COST : int
    The cost of a person being in hospital per person per day
  
  Vaccination Parameters
  ----------------------
  VACCINATION_ENABLED : bool
    Whether vaccination is enabled
  VACCINATION_RATE : float
    The percentage of suseptible population which gets vaccinated in a day
  VACCINATION_COST : int
    The cost of one vaccination

  Lockdown Parameters
  ---------------------
  LOCKDOWN_ENABLED : bool
    Whether lockdown is enabled
  LOCKDOWN_LEVEL : float
    The percentage of infected population at which lockdown is enabled
  LOCKDOWN_COST : int
    The cost of lockdown per person per day
  
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
    self.POPULATION_SIZE = 1000
    self.POPULATION_DEMOGRAPHICS = [0.35, 0.8, 0.95, 1]
    self.SIMULATION_LENGTH = 180
    self.CONTACT_RADIUS = 0.1
    self.TIME_PER_FRAME = 0.2
    self.GRID_SIZE = 3
    self.CELL_SIZE = 1 / self.GRID_SIZE
    self.MAX_MOVEMENT = 0.05
    self.TRAVEL_RATE = 0.2
    self.COMORBIDITY_COEFFICIENTS = [0.7, 0.9, 1.1, 1.3]
    self.RANDOM_SEED = 0
    self.GRID_PROBABILITIES = [0.1312769922816259, 0.1390833168942316, 0.3045853365542704, 0.4356598378729931, 0.5622315487782497, 0.661694550602876, 0.7233137507793976, 0.9097747150485921, 1.0]
    self.TRAVEL_PROBABILITES = [[[0.0, 0.03379616975731785, 0.09684667359660301, 0.1197835952460493, 0.2327447137437878, 0.2804888029790266, 0.5027118070654588, 0.8066508042749484, 1.0], [0.07617464387523151, 0.07617464387523151, 0.1816558923223277, 0.2011513865706794, 0.3661371224033967, 0.4099182852265705, 0.4729618050387855, 0.8450845232185137, 1.0], [0.007084892419548851, 0.02254751484538488, 0.02254751484538488, 0.1253911697157372, 0.1826306328760722, 0.3964735255124403, 0.5728002010793476, 0.8047586243571166, 1.0]], [[0.03963295365806974, 0.07031976956785578, 0.08912460024153888, 0.08912460024153888, 0.2954183687537309, 0.4212762715742198, 0.6660293348168977, 0.7842558116229676, 1.0], [0.02562452542293952, 0.0533570645169343, 0.1613431889627293, 0.2678741587261874, 0.2678741587261874, 0.432276125986011, 0.459385995049083, 0.611547730638288, 1.0], [0.02042102824622067, 0.02186963518242044, 0.05069576323004668, 0.06189596835785194, 0.2758427588612641, 0.2758427588612641, 0.4974713468332541, 0.7071080130626465, 1.0]], [[0.01209819766876787, 0.03429260143187643, 0.1212210824583032, 0.2058316920429337, 0.2198178316298769, 0.5740967032209175, 0.5740967032209175, 0.8238039618231251, 1.0], [0.01668570530274214, 0.0430169617796957, 0.1670251342599318, 0.3240885734660761, 0.428417517236946, 0.4326324326576926, 0.7148699939551761, 0.7148699939551761, 1.0], [0.001539249321669094, 0.04380406500777381, 0.09796927008080859, 0.1973453443620199, 0.3043932552419717, 0.4109349467573427, 0.5938183708989476, 1.0, 1.0]]]

    # State transition related parameters
    self.INITIAL_INFECTED = 2
    self.INFECTION_RATE = 0.6
    self.INCUBATION_PERIOD = 5
    self.INFECTION_PERIOD = 10
    self.MORTALITY_RATE = 0.3
    self.IMMUNITY_PERIOD = 30

    # Intervention related parameters
    self.RULE_COMPLIANCE_RATE = 1.0
    self.HOSPITAL_CAPACITY = 0.0
    self.HOSPITALIZATION_RATE = 5 * self.MORTALITY_RATE
    self.HOSPITALIZATION_COST = 5000

    # Vaccination related parameters
    self.VACCINATION_ENABLED = False
    self.VACCINATION_RATE = 0.01
    self.VACCINATION_COST = 1000

    # Lockdown related parameters
    self.LOCKDOWN_ENABLED = False
    self.LOCKDOWN_LEVEL = 0.5
    self.LOCKDOWN_COST = 500

    # Hygiene related parameters
    self.HYGIENE_ENABLED = False
    self.HYGIENE_RATE = 0.6
    self.HYGIENE_COST = 100

    # Travel restrictions related parameters
    self.TRAVEL_RESTRICTIONS_ENABLED = False
    self.TRAVEL_RESTRICTIONS_COST = 200

    # Change the value for each parameter in kwargs from default
    for param, value in kwargs.items():
      exec(f'self.{param} = {value}')