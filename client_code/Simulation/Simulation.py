from random import random, uniform
from math import sqrt
from time import time

from Frame import Frame # type: ignore
from Person import Person # type: ignore
from Params import Params # type: ignore

class Simulation:
  """Parameters and methods for the simulation.

  Attributes
  ----------
  self.PARAMS : Params
    The parameters of the simulation

  Methods
  -------
  __init__()
    Initialized the simulation with some properties
  run()
    Runs the current simulation
  """

  def __init__(self, PARAMS):
    """"Initialized the simulation

    Intializes the simulation with some basic properties

    Parameters
    ----------
    PARAMS : Params
      The parameters of the simulation

    Returns
    -------
    None
    """

    self.PARAMS = PARAMS

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

    # Create the first frame
    # Intialize the population list with people and whether they follow rules
    people = []
    for _ in range(self.PARAMS.POPULATION_SIZE):
      if self.PARAMS.QUARANTINE_ENABLED:
        people.append(Person(
          uniform(self.PARAMS.QUARANTINE_SIZE, 1), 
          uniform(self.PARAMS.QUARANTINE_SIZE, 1), 
          random() < self.PARAMS.RULE_COMPLIANCE_RATE
        ))
      else:
        people.append(Person(
          random(), 
          random(), 
          random() < self.PARAMS.RULE_COMPLIANCE_RATE
        ))

    # There are some people who are exposed at the beginning
    for infectedCount in range(self.PARAMS.INITIAL_INFECTED):
      people[infectedCount].state = Person.EXPOSED
      people[infectedCount].framesSinceInfection = 0
    for infectedCount in range(self.PARAMS.INITIAL_INFECTED, self.PARAMS.POPULATION_SIZE):
      people[infectedCount].state = Person.SUSCEPTIBLE

    currFrame = Frame(people)
    yield currFrame

    for frameCount in range(self.PARAMS.SIMULATION_LENGTH):
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
    self.findExposed(frame)
    self.findInfected(frame)
    self.findRecovered(frame)
    
    if self.PARAMS.VACCINATION_ENABLED:
      self.vaccinate(frame)

    return Frame(frame.people)
  
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

    # Iterate through all people and move them to a random location close by
    for person in frame.people:
      if person.state != Person.DEAD:
        # If social distancing is enabled, reduce the movement
        if self.PARAMS.SOCIAL_DISTANCING_ENABLED and person.followsRules:
          maxMovement = self.PARAMS.SOCIAL_DISTANCING_MAX_MOVEMENT
        else:
          maxMovement = self.PARAMS.MAX_MOVEMENT

        # Change the position of the person by a random amount
        person.x += uniform(-maxMovement, maxMovement)
        person.y += uniform(-maxMovement, maxMovement)
        
        # Make sure it doesn't excedd the bounds
        if person.isQuarantined:
          person.x = max(0, min(self.PARAMS.QUARANTINE_SIZE, person.x))
          person.y = max(0, min(self.PARAMS.QUARANTINE_SIZE, person.y))
        elif self.PARAMS.QUARANTINE_ENABLED:
          person.x = max(self.PARAMS.QUARANTINE_SIZE, min(1, person.x))
          person.y = max(self.PARAMS.QUARANTINE_SIZE, min(1, person.y))
        else:
          person.x = max(0, min(1, person.x))
          person.y = max(0, min(1, person.y))

  def findExposed(self, frame):
    """Find out who will be exposed to the virus next
    
    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    
    Returns
    -------
    None
    """

    # Find the people who are susceptible and infected
    suseptibleGroup = [frame.people[i] for i in frame.stateGroups[Person.SUSCEPTIBLE.id]]
    infectedGroup = [frame.people[i] for i in frame.stateGroups[Person.INFECTED.id]]
    
    # Find if any of the two groups are in contact and the disease spreads
    for infectedPerson in infectedGroup:
      for susceptiblePerson in suseptibleGroup:
        dist = sqrt(
          abs(infectedPerson.x - susceptiblePerson.x) ** 2 + 
          abs(infectedPerson.y - susceptiblePerson.y) ** 2
        )
        if dist <= self.PARAMS.CONTACT_RADIUS and random() < self.PARAMS.INFECTION_RATE:
          # The disease spreads to the susceptible person and he becomes exposed
          susceptiblePerson.state = Person.EXPOSED
          susceptiblePerson.framesSinceInfection = 0

  def findInfected(self, frame):
    """Find out who will be infected in the next frame.

    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    
    Returns
    -------
    None
    """

    # Iterate through all people and find those who are exposed
    # Find if they become infected
    for personCount in frame.stateGroups[Person.EXPOSED.id]:
      person = frame.people[personCount]
      person.framesSinceInfection += 1
      if person.framesSinceInfection >= self.PARAMS.INCUBATION_PERIOD:
        # The person becomes symptomatic
        person.state = Person.INFECTED
        person.isQuarantined = self.PARAMS.QUARANTINE_ENABLED and random() < self.PARAMS.QUARANTINE_RATE

  def findRecovered(self, frame):
    """Find out who will be recovered / dead next
    
    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    
    Returns
    -------
    None
    """

    # Iterate through all people and find those who are infected
    # Find if they have no time left for disease
    for personCount in frame.stateGroups[Person.INFECTED.id]:
      person = frame.people[personCount]
      person.framesSinceInfection += 1
      if person.framesSinceInfection >= self.PARAMS.INFECTION_PERIOD:
        # Find if the person recovers or dies
        person.framesSinceInfection = -1
        person.isQuarantined = False
        if random() < self.PARAMS.MORTALITY_RATE:
          person.state = Person.DEAD
        else:
          person.state = Person.RECOVERED

  def vaccinate(self, frame):
    """"Find ou who is vaccinated

    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    
    Returns
    -------
    None
    """

    for personCount in frame.stateGroups[Person.SUSCEPTIBLE.id]:
      person = frame.people[personCount]
      if random() < self.PARAMS.VACCINATION_RATE:
        person.state = Person.VACCINATED

if __name__ == '__main__':
  # Only performed when this file is run directly
  from matplotlib import pyplot as plt

  def drawFramesMatplotlib(frames, PARAMS):
    """Draws the frame in a matplotlib graph.

    Parameters
    ----------
    frame : list(Frame)
      The list of frames that we have to display
    frameCount : int
      The current frameCount
    PARAMS : Params
      The parameters of the simulation

    Returns
    -------
    None
    """

    # Initialize arrays for graphing the results
    graphXData = []
    graphYData = [[] for _ in Person.states]

    # Get the data for the X and Y axes
    for frameCount, frame in enumerate(frames):
      graphXData.append(frameCount)
      for stateID, stateGroup in enumerate(frame.stateGroups):
        graphYData[stateID].append(len(stateGroup))

    # Add the plots to the graph
    for stateID, stateCountData in enumerate(graphYData):
      plt.plot(
        graphXData,
        stateCountData,
        label = Person.states[stateID].name,
        color = Person.states[stateID].color,
      )

    # Show the matplotlib plots
    plt.ylim(0, PARAMS.POPULATION_SIZE)
    plt.show()

  # Created a simulation object and runs the simulation
  params = Params(
    POPULATION_SIZE = 1000,
    VACCINATION_ENABLED = True,
    SOCIAL_DISTANCING_ENABLED = False,
    QUARANTINE_ENABLED = True
  )
  simulation = Simulation(params)
  startTime = time()
  frames = list(simulation.run())
  print(f'Time taken: {time() - startTime:.2f}s')
  drawFramesMatplotlib(frames, params)