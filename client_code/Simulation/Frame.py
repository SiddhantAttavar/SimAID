import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from Person import Person # type: ignore

class Frame:
  '''Stores information about each frame in the simulation.

  Attributes
  ----------
  grid : List[List[List[Person]]]
    list of people in each cell of the grid
  visitingGrid : List[List[List[Person]]]
    list of people in each cell of the grid who are visiting the cell
  isLockedDown : List[List[bool]]
    Whether the cell is under lockdown
  stateGroupss : List[List[Tuple[int, int, int]]]
    list of indexes of the people in each states
  effectiveReproductionNumber : float
    Effective reproduction number of the disease (Re)
  averageContacts : float
    Average number of susceptible contacts per infected person
  reproductiveSum : int
  reproductiveSum : int
    Number of agents infected by agents that have stopped being infected
  contactSum : int
    Number of susceptible agents contacted by infected agents
  removedAgents : int
  removedAgents : int
    Number of infected agents that have recovered / died
  doublingTime : float
  doublingTime : float
    Time it takes for the disease to double (Td)
  hospitalOccupancy : float
    Percentage of the population that is in the hospital

  Methods
  -------
  __init__(people)
    Initializes the Frame object with some properties
  '''

  def __init__(self, grid, params):
    '''Sets some initial parameters for the frame.
    
    Parameters
    ----------
    people : list(Person.State)
      list of people in the population in the current frame
    
    Returns
    -------
    None
    '''

    # Initialize the variables and set every state in Person.State to an empty list
    self.grid = grid
    self.visitingGrid = [[[] for i in range(params.GRID_SIZE)] for j in range(params.GRID_SIZE)]
    self.isLockedDown = [[False for i in range(params.GRID_SIZE)] for j in range(params.GRID_SIZE)]
    self.stateGroups = [[] for _ in Person.states]

    # Initialize metrics
    self.effectiveReproductionNumber = 0
    self.averageContacts = 0
    self.reproductiveSum = 0
    self.contactSum = 0
    self.removedAgents = 0
    self.doublingTime = 0
    self.hospitalOccupancy = 0

    # Iterate through the list and add the person to the state group
    for row in range(params.GRID_SIZE):
      for col in range(params.GRID_SIZE):
        for personCount, person in enumerate(self.grid[row][col]):
          self.stateGroups[person.state.id].append((row, col, personCount))