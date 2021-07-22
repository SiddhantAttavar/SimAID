import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from random import random, uniform, randrange
from bisect import bisect_left as insertLeft

from Frame import Frame # type: ignore
from Person import Person # type: ignore
from Params import Params # type: ignore
from Transitions import Transitions # type: ignore
from Interventions import Interventions # type: ignore
from Utils import Utils # type: ignore

class Simulation:
  '''Parameters and methods for the simulation.

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
  '''

  def __init__(self, params):
    '''Initialized the simulation

    Intializes the simulation with some basic properties

    Parameters
    ----------
    params : Params
      The parameters of the simulation

    Returns
    -------
    None
    '''

    self.params = params

  def run(self):
    '''Run the simulation.

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
    '''

    # Create the probability matrix for the grid
    self.params.GRID_PROBABILITIES = [random() for _ in range(self.params.GRID_SIZE ** 2)]

    # Find the cumulative sum for each cell
    for i in range(1, self.params.GRID_SIZE * self.params.GRID_SIZE):
      self.params.GRID_PROBABILITIES[i] += self.params.GRID_PROBABILITIES[i - 1]

    # Scale all probabilities by the sum of probabilities
    for i in range(self.params.GRID_SIZE * self.params.GRID_SIZE):
      self.params.GRID_PROBABILITIES[i] /= self.params.GRID_PROBABILITIES[-1]

    # Create the probability matrix for travel between cells
    # Iterate through all cells
    self.params.TRAVEL_PROBABILITES = []
    for rowCount in range(self.params.GRID_SIZE):
      self.params.TRAVEL_PROBABILITES.append([])
      for colCount in range(self.params.GRID_SIZE):
        # For each cell create probabilities
        travelProbabilites = [random() for _ in range(self.params.GRID_SIZE ** 2)]

        # The probability of travelling from a cell to itself is 0
        travelProbabilites[rowCount * self.params.GRID_SIZE + colCount] = 0

        # Add probability factor to the probability matrix
        for i in range(self.params.GRID_SIZE * self.params.GRID_SIZE):
          travelProbabilites[i] *= self.params.GRID_PROBABILITIES[i]

        # Find the cumulative sum for each cell
        for i in range(1, self.params.GRID_SIZE * self.params.GRID_SIZE):
          travelProbabilites[i] += travelProbabilites[i - 1]
        
        # Scale all probabilities by the sum of probabilities
        for i in range(self.params.GRID_SIZE * self.params.GRID_SIZE):
          travelProbabilites[i] /= travelProbabilites[-1]
        
        # Add the probabilities to the probability matrix
        self.params.TRAVEL_PROBABILITES[rowCount].append(travelProbabilites)

    # Create the first frame
    # Intialize the population list with people and whether they follow rules
    grid = [[[] for i in range(self.params.GRID_SIZE)] for j in range(self.params.GRID_SIZE)]
    for _ in range(self.params.POPULATION_SIZE):
      # Find a random cell for the person
      cellRow, cellCol = Utils.getRandomCell(self.params, self.params.GRID_PROBABILITIES)

      # Add the person to the grid
      grid[cellRow][cellCol].append(Person(
        (cellRow, cellCol),
        self.params.CELL_SIZE * cellCol + random() / self.params.GRID_SIZE,
        self.params.CELL_SIZE * cellRow + random() / self.params.GRID_SIZE,
        random() < self.params.RULE_COMPLIANCE_RATE,
        Person.SUSCEPTIBLE,
        insertLeft(self.params.POPULATION_DEMOGRAPHICS, random())
      ))

    # There are some people who are exposed at the beginning
    done = set()
    for _ in range(self.params.INITIAL_INFECTED):
      cellRow, cellCol = Utils.getRandomCell(self.params, self.params.GRID_PROBABILITIES)
      personCount = randrange(len(grid[cellRow][cellCol]))
      key = (cellRow, cellCol, personCount)

      if key not in done:
        done.add(key)
        grid[cellRow][cellCol][personCount].state = Person.EXPOSED

    currFrame = Frame(grid, self.params)
    yield currFrame

    for _ in range(self.params.SIMULATION_LENGTH):
      # Then we need to build the Frame object to yield
      currFrame = self.nextFrame(currFrame)
      yield currFrame

  def nextFrame(self, frame):
    '''Calculate the next frame of the simulation.

    Parameters
    ----------
    frame : Frame
      The current frame of the simulation

    Returns
    -------
    Frame
      The next frame in the simulation
    '''

    self.movePeople(frame)

    if self.params.VACCINATION_ENABLED:
      Interventions.vaccinate(frame, self.params)
    if self.params.LOCKDOWN_ENABLED:
      Interventions.lockdown(frame, self.params)

    Transitions.findExposed(frame, self.params)
    Transitions.findInfected(frame, self.params)
    Transitions.findRecovered(frame, self.params)
    Transitions.findSusceptible(frame, self.params)

    # Iterate through all people and increment the frames since last state
    for row in frame.grid:
      for cell in row:
        for person in cell:
          person.framesSinceLastState += 1

    res = Frame(frame.grid, self.params)
    res.isLockedDown = frame.isLockedDown.copy()

    return res
  
  def movePeople(self, frame):
    '''Move the people around
    
    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    
    Returns
    -------
    None
    '''

    # Clear the visiting grid
    for rowCount in range(self.params.GRID_SIZE):
      for colCount in range(self.params.GRID_SIZE):
        frame.visitingGrid[rowCount][colCount].clear()
    
    # Find the number of cells not under lockdown
    cellsToTravelTo = sum(sum(row) for row in frame.isLockedDown)

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

          if (((not person.followsRules or not self.params.TRAVEL_RESTRICTIONS_ENABLED) or 
              cellsToTravelTo - (not frame.isLockedDown[rowCount][colCount]) > 0) and 
              random() < self.params.TRAVEL_RATE):
            # The person is travelling to a different cell
            cellRow, cellCol = Utils.getRandomCell(
              self.params, 
              self.params.TRAVEL_PROBABILITES[rowCount][colCount]
            )
            if self.params.TRAVEL_RESTRICTIONS_ENABLED:
              while frame.isLockedDown[cellCol][cellRow]:
                cellRow, cellCol = Utils.getRandomCell(
                  self.params, 
                  self.params.TRAVEL_PROBABILITES[rowCount][colCount]
                )
            
            frame.visitingGrid[cellRow][cellCol].append(person)
            person.isVisiting = True

            # Continue to the next cell, because there is no movement
            continue
          else:
            person.isVisiting = False

          # Reset the person's location to home
          person.x, person.y = person.home

          # Change the position of the person by a random amount
          person.x += uniform(-self.params.MAX_MOVEMENT, self.params.MAX_MOVEMENT)
          person.y += uniform(-self.params.MAX_MOVEMENT, self.params.MAX_MOVEMENT)

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
    LOCKDOWN_ENABLED = True,
    HYGIENE_ENABLED = False,
    TRAVEL_RESTRICTIONS_ENABLED = False
  )
  
  simulation = Simulation(params)
  startTime = time()
  frames = list(simulation.run())
  print(f'Time taken: {time() - startTime:.2f}s')

  Utils.drawFramesMatplotlib(frames, params)