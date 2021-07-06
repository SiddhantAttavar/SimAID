import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from random import random, uniform, randrange

from Frame import Frame # type: ignore
from Person import Person # type: ignore
from Params import Params # type: ignore
from Transitions import Transitions # type: ignore
from Interventions import Interventions # type: ignore
from Utils import Utils # type: ignore

class Simulation:
  """Parameters and methods for the simulation.

  Attributes
  ----------
  params : Params
    The parameters of the simulation
  transitions : Transitions
    The methods for the transitions of the simulation

  Methods
  -------
  __init__()
    Initialized the simulation with some properties
  run()
    Runs the current simulation
  nextFrame(frame)
    Calculates the next frame of the simulation
  """

  def __init__(self, params):
    """"Initialized the simulation

    Intializes the simulation with some basic properties

    Parameters
    ----------
    params : Params
      The parameters of the simulation

    Returns
    -------
    None
    """

    self.params = params

  def run(self):
    """Run the simulation.

    Run an agent based simulation based on the
    configuration of the current simulation.

    Parameters
    ----------

    Yields
    ------
    Frame
      Constantly yields frames of simulation as they are calculated

    Returns
    -------
    None
    """

    # Create the probability matrix for the grid
    self.params.GRID_PROBABILITIES = [random() for _ in range(self.params.GRID_SIZE ** 2)]

    # Find the cumulative sum for each cell
    for i in range(1, self.params.GRID_SIZE * self.params.GRID_SIZE):
      self.params.GRID_PROBABILITIES[i] += self.params.GRID_PROBABILITIES[i - 1]

    # Scale all probabilities by the sum of probabilities
    for i in range(self.params.GRID_SIZE * self.params.GRID_SIZE):
      self.params.GRID_PROBABILITIES[i] /= self.params.GRID_PROBABILITIES[-1]

    # Create the first frame
    # Intialize the population list with people and whether they follow rules
    grid = [[[] for i in range(self.params.GRID_SIZE)] for j in range(self.params.GRID_SIZE)]
    for _ in range(self.params.POPULATION_SIZE):
      # Find a random cell for the person
      cellRow, cellCol = Utils.getRandomCell(self.params)

      # Add the person to the grid
      grid[cellRow][cellCol].append(Person(
        (cellRow, cellCol),
        self.params.CELL_SIZE * cellCol + random() / self.params.GRID_SIZE,
        self.params.CELL_SIZE * cellRow + random() / self.params.GRID_SIZE,
        random() < self.params.RULE_COMPLIANCE_RATE,
        Person.SUSCEPTIBLE
      ))

    # There are some people who are exposed at the beginning
    done = set()
    for _ in range(self.params.INITIAL_INFECTED):
      cellRow, cellCol = Utils.getRandomCell(self.params)
      personCount = randrange(len(grid[cellRow][cellCol]))
      key = (cellRow, cellCol, personCount)

      if key not in done:
        done.add(key)
        grid[cellRow][cellCol][personCount].state = Person.EXPOSED
        grid[cellRow][cellCol][personCount].framesSinceInfection = 0

    currFrame = Frame(grid, self.params)
    yield currFrame

    for _ in range(self.params.SIMULATION_LENGTH):
      # Then we need to build the Frame object to yield
      currFrame = self.nextFrame(currFrame)
      yield currFrame

  def nextFrame(self, frame):
    """Calculate the next frame of the simulation.

    Parameters
    ----------
    frame : Frame
      The current frame of the simulation

    Returns
    -------
    Frame
      The next frame in the simulation
    """

    self.movePeople(frame)
    Transitions.findExposed(frame, self.params)
    Transitions.findInfected(frame, self.params)
    Transitions.findRecovered(frame, self.params)
    
    if self.params.VACCINATION_ENABLED:
      Interventions.vaccinate(frame, self.params)

    return Frame(frame.grid, self.params)
  
  def movePeople(self, frame):
    """Move the people around
    
    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    
    Returns
    -------
    None
    """

    # Clear the visiting grid
    for rowCount in range(self.params.GRID_SIZE):
      for colCount in range(self.params.GRID_SIZE):
        frame.visitingGrid[rowCount][colCount].clear()

    # Iterate through all cells
    for rowCount, row in enumerate(frame.grid):
      # Find the limits of the row
      yMin = rowCount * self.params.CELL_SIZE
      yMax = yMin + self.params.CELL_SIZE
      
      for colCount, cell in enumerate(row):
        # Find the limits for the cell
        xMin = colCount * self.params.CELL_SIZE
        xMax = xMin + self.params.CELL_SIZE
        
        # Iterate through all people and move them to a random location in the same cell
        for person in cell:
          if person.state == Person.DEAD:
            # Dead people do not move
            continue

          if random() < self.params.TRAVEL_RATE:
            # The person is travelling to a different cell
            cellRow, cellCol = Utils.getRandomCell(self.params)
            frame.visitingGrid[cellRow][cellCol].append(person)
            person.isVisiting = True
            continue
          else:
            person.isVisiting = False
          
          # If social distancing is enabled, reduce the movement
          if self.params.SOCIAL_DISTANCING_ENABLED and person.followsRules:
            maxMovement = self.params.SOCIAL_DISTANCING_MAX_MOVEMENT
          else:
            maxMovement = self.params.MAX_MOVEMENT

          # Reset the person's location to home
          person.x, person.y = person.home

          # Change the position of the person by a random amount
          person.x += uniform(-maxMovement, maxMovement)
          person.y += uniform(-maxMovement, maxMovement)

          person.x = min(xMax, max(xMin, person.x))
          person.y = min(yMax, max(yMin, person.y))

if __name__ == '__main__':
  # Only performed when this file is run directly
  # Create a simulation object and runs the simulation
  from time import time

  # Parameters for running the simulation
  params = Params(
    POPULATION_SIZE = 5000,
    VACCINATION_ENABLED = False,
    SOCIAL_DISTANCING_ENABLED = False,
    QUARANTINE_ENABLED = False,
    HYGIENE_ENABLED = False
  )
  
  simulation = Simulation(params)
  startTime = time()
  frames = list(simulation.run())
  print(f'Time taken: {time() - startTime:.2f}s')

  Utils.drawFramesMatplotlib(frames, params)