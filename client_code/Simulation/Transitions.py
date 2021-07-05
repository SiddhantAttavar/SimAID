from random import random, uniform
from math import sqrt

from Person import Person # type: ignore

class Transitions:
  """This class contiains functions for the transition between states

  Attributes
  ----------

  Methods
  -------
  findExposed(frame, params)
    Finds out who will be exposed to the virus
  findInfected(frame, params)
    Finds out who will be infected
  findRemoved(frame, params)
    Finds out who will be recovered / dead
  vaccinate(frame, params)
    Finds out who is vaccinated
  """

  @staticmethod
  def findExposed(frame, params):
    """Find out who will be exposed to the virus next
    
    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    params : Params
      The parameters of the simulation
    
    Returns
    -------
    None
    """

    # Find the people who are susceptible and infected
    suseptibleGroup = []
    for ind in frame.stateGroups[Person.SUSCEPTIBLE.id]:
      suseptibleGroup.append(frame.grid[ind[0]][ind[1]][ind[2]])
    
    infectedGroup = []
    for ind in frame.stateGroups[Person.INFECTED.id]:
      infectedGroup.append(frame.grid[ind[0]][ind[1]][ind[2]])
    
    # Find if any of the two groups are in contact and the disease spreads
    for infectedPerson in infectedGroup:
      for susceptiblePerson in suseptibleGroup:
        dist = sqrt(
          abs(infectedPerson.x - susceptiblePerson.x) ** 2 + 
          abs(infectedPerson.y - susceptiblePerson.y) ** 2
        )

        infectionRate = params.INFECTION_RATE
        if params.HYGIENE_ENABLED and susceptiblePerson.followsRules and infectedPerson.followsRules:
          infectionRate *= params.HYGIENE_RATE

        if dist <= params.CONTACT_RADIUS and random() < infectionRate:
          # The disease spreads to the susceptible person and he becomes exposed
          susceptiblePerson.state = Person.EXPOSED
          susceptiblePerson.framesSinceInfection = 0

  @staticmethod
  def findInfected(frame, params):
    """Find out who will be infected in the next frame.

    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    params : Params
      The parameters of the simulation
    
    Returns
    -------
    None
    """

    # Iterate through all people and find those who are exposed
    # Find if they become infected
    for row, col, personCount in frame.stateGroups[Person.EXPOSED.id]:
      person = frame.grid[row][col][personCount]
      person.framesSinceInfection += 1
      if person.framesSinceInfection >= params.INCUBATION_PERIOD:
        # The person becomes symptomatic
        person.state = Person.INFECTED
        if params.QUARANTINE_ENABLED and random() < params.QUARANTINE_RATE:
          person.isQuarantined = True
          person.x = uniform(0, params.QUARANTINE_SIZE)
          person.y = uniform(0, params.QUARANTINE_SIZE)
  
  @staticmethod
  def findRecovered(frame, params):
    """Find out who will be recovered / dead next
    
    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    params : Params
      The parameters of the simulation
    
    Returns
    -------
    None
    """

    # Iterate through all people and find those who are infected
    # Find if they have no time left for disease
    for row, col, personCount in frame.stateGroups[Person.INFECTED.id]:
      person = frame.grid[row][col][personCount]
      person.framesSinceInfection += 1
      if person.framesSinceInfection >= params.INFECTION_PERIOD:
        # Find if the person recovers or dies
        person.framesSinceInfection = -1
        person.isQuarantined = False
        if random() < params.MORTALITY_RATE:
          person.state = Person.DEAD
        else:
          person.state = Person.RECOVERED