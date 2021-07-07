import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import server

class Person:
  '''Stores variables and methods for Person.

  The person class is used to store variables
  and methods for each person / agent
  This includes properties like position, infection status,
  comorbidities, etc. and methods like move etc.

  Attributes
  ----------
  cell : tuple(int)
    The home cell of the person
  x : int
    An integer which stores the X-coordinate of the person
  y : int
    An integer which stores the Y-coordinate of the person
  home : tuple(int)
    The location of the home of the person
  state : State
    A variable which stores the current state of the person
  framesSinceLastState : int
    The number of days since the person was infected (default -1)
  followsRules : bool
    whether the person follows rules like social distancing and wearing mask
  isVisiting : bool
    Whether the person is visiting another cell

  STATES
  ------
    SUSCEPTIBLE : The person can contract the disease
    EXPOSED : The person has contracted the disease but is asymptomatic
    INFECTED : The person has contracted the disease and is symptomatic
    RECOVERED - The person no longer has the disease and is immune
    DEAD - The person has died from the disease
    VACCINATED - The person has been vaccinated and is immune

  Methods
  -------
  __init__()
    Initializes the person object with some properties

  Classes
  -------
  State
    The state of the person
  '''

  class State:
    '''Enum which contains various states of the disease and their colors.
    
    Attributes
    ----------
    name : str
      The name of the state
    stateID : int
      The ID of the current state
    color : str
      The color of the current state
    
    Methods
    -------
    __init__()
      Initalizes the State
    __eq__()
      Checks if two states are the same
    __hash__()
      Hashes the state
    '''

    def __init__(self, name, stateID, color):
      '''Sets some initial parameters for the state
      
      Parameters
      ----------
      state : str
        The state of the state object
      
      Returns
      -------
      None
      '''

      self.name = name
      self.id = stateID
      self.color = color
    
    def __eq__(self, other):
      '''Checks if 2 states are equal
      
      Parameters
      ----------
      other : State
        The other state
      
      Returns
      -------
      bool
        Whether the states are equal
      '''

      return self.id == other.id
    
    def __hash__(self):
      '''Hashes the state for use in dict or set
      
      Parameters
      ----------

      Returns
      -------
      int
        The hash value
      '''

      return self.id
  
  # Define the states
  SUSCEPTIBLE = State('SUSCEPTIBLE', 0, 'green')
  EXPOSED = State('EXPOSED', 1, 'orange')
  INFECTED = State('INFECTED', 2, 'red')
  RECOVERED = State('RECOVERED', 3, 'blue')
  DEAD = State('DEAD', 4, 'gray')
  VACCINATED = State('VACCINATED', 5, 'yellow')

  states = [
    SUSCEPTIBLE,
    EXPOSED,
    INFECTED,
    RECOVERED,
    DEAD,
    VACCINATED
  ]

  def __init__(self, cell, x, y, followsRules, state):
    '''Sets some initial parameters for the person.

    Parameters
    ----------
    startX : int
      The starting X coordinate
    startY : int
      The starting Y coordinate
    
    Returns
    -------
    None
    '''

    self.cell = cell
    self.x = x
    self.y = y
    self.home = (self.x, self.y)
    self.state = state
    self.framesSinceLastState = 0
    self.followsRules = followsRules