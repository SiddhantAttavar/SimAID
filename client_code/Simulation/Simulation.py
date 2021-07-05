from random import random, uniform

from Frame import Frame # type: ignore
from Person import Person # type: ignore
from Params import Params # type: ignore
from Transitions import Transitions # type: ignore
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

    # Create the first frame
    # Intialize the population list with people and whether they follow rules
    people = []
    for _ in range(self.params.POPULATION_SIZE):
      if self.params.QUARANTINE_ENABLED:
        # Keep moving the person until we find a location 
        # not in the quarantine zone
        initLoc = (random(), random())
        while (initLoc[0] < self.params.QUARANTINE_SIZE and 
              initLoc[1] < self.params.QUARANTINE_SIZE):
          initLoc = (random(), random())
        
        people.append(Person(
          *initLoc,
          random() < self.params.RULE_COMPLIANCE_RATE
        ))
      else:
        people.append(Person(
          random(), 
          random(), 
          random() < self.params.RULE_COMPLIANCE_RATE
        ))

    # There are some people who are exposed at the beginning
    for infectedCount in range(self.params.INITIAL_INFECTED):
      people[infectedCount].state = Person.EXPOSED
      people[infectedCount].framesSinceInfection = 0
    for infectedCount in range(self.params.INITIAL_INFECTED, self.params.POPULATION_SIZE):
      people[infectedCount].state = Person.SUSCEPTIBLE

    currFrame = Frame(people)
    yield currFrame

    for frameCount in range(self.params.SIMULATION_LENGTH):
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
        if self.params.SOCIAL_DISTANCING_ENABLED and person.followsRules:
          maxMovement = self.params.SOCIAL_DISTANCING_MAX_MOVEMENT
        else:
          maxMovement = self.params.MAX_MOVEMENT

        # Change the position of the person by a random amount
        person.x += uniform(-maxMovement, maxMovement)
        person.y += uniform(-maxMovement, maxMovement)
        
        # Make sure it doesn't excedd the bounds
        if person.isQuarantined:
          person.x = max(0, min(self.params.QUARANTINE_SIZE, person.x))
          person.y = max(0, min(self.params.QUARANTINE_SIZE, person.y))
        elif self.params.QUARANTINE_ENABLED:
          person.x = min(1, person.x)
          person.y = min(1, person.y)

          # If the person is in the quarantined zone move the person out
          if (person.x < self.params.QUARANTINE_SIZE and 
              person.y < self.params.QUARANTINE_SIZE):
            xDiff = self.params.QUARANTINE_SIZE - person.x
            yDiff = self.params.QUARANTINE_SIZE - person.y

            if xDiff < yDiff:
              person.x = self.params.QUARANTINE_SIZE
            else:
              person.y = self.params.QUARANTINE_SIZE
        else:
          person.x = max(0, min(1, person.x))
          person.y = max(0, min(1, person.y))

if __name__ == '__main__':
  # Only performed when this file is run directly
  # Create a simulation object and runs the simulation
  from time import time

  # Parameters for running the simulation
  params = Params(
    POPULATION_SIZE = 1000,
    VACCINATION_ENABLED = False,
    SOCIAL_DISTANCING_ENABLED = False,
    QUARANTINE_ENABLED = False,
    HYGEINE_ENABLED = False
  )
  
  simulation = Simulation(params)
  startTime = time()
  frames = list(simulation.run())
  print(f'Time taken: {time() - startTime:.2f}s')

  Utils.drawFramesMatplotlib(frames, params)