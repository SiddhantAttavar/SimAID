import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from random import random, uniform
from math import sqrt

from Person import Person # type: ignore

class Transitions:
  '''This class contiains functions for the transition between states

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
  findSusceptible(frame, params)
    Find out who loses immunity
  '''

  @staticmethod
  def findExposed(frame, params):
    '''Find out who will be exposed to the virus next
    
    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    params : Params
      The parameters of the simulation
    
    Returns
    -------
    int
      Cost of hygiene measures if enabled
    '''

    # Iterate through all cells
    cost = 0
    for rowCount, row in enumerate(frame.grid):
      for colCount, cell in enumerate(row):
        # Find the people who are susceptible and infected
        susceptibleGroup = []
        infectedGroup = []

        for person in cell:
          if not person.isVisiting:
            if person.state == Person.SUSCEPTIBLE:
              susceptibleGroup.append(person)
            elif person.state == Person.INFECTED:
              infectedGroup.append(person)
        for person in frame.visitingGrid[rowCount][colCount]:
          if person.state == Person.SUSCEPTIBLE:
            susceptibleGroup.append(person)
          elif person.state == Person.INFECTED:
            infectedGroup.append(person)

        # Iterate through all pairs of infected and susceptible movePeople
        # Find when the infection is transmitted
        for susceptiblePerson in susceptibleGroup:
          for infectedPerson in infectedGroup:
            dist = sqrt(
              abs(infectedPerson.x - susceptiblePerson.x) ** 2 + 
              abs(infectedPerson.y - susceptiblePerson.y) ** 2
            )

            infectionRate = params.INFECTION_RATE
            if (params.HYGIENE_ENABLED and 
                (susceptiblePerson.followsRules and infectedPerson.followsRules)):
              infectionRate *= params.HYGIENE_RATE

            if dist <= params.CONTACT_RADIUS and random() < infectionRate:
              # The disease spreads to the susceptible person and he becomes exposed
              susceptiblePerson.state = Person.EXPOSED
              susceptiblePerson.framesSinceLastState = 0

              # Add to cost
              cost += params.HYGIENE_COST
    
    # Return cost
    return cost

  @staticmethod
  def findInfected(frame, params):
    '''Find out who will be infected in the next frame.

    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    params : Params
      The parameters of the simulation
    
    Returns
    -------
    None
    '''

    # Iterate through all people and find those who are exposed
    # Find if they become infected
    for row, col, personCount in frame.stateGroups[Person.EXPOSED.id]:
      person = frame.grid[row][col][personCount]
      if person.framesSinceLastState >= params.INCUBATION_PERIOD:
        # The person becomes symptomatic
        person.state = Person.INFECTED
        person.framesSinceLastState = 0
  
  @staticmethod
  def findRecovered(frame, params):
    '''Find out who will be recovered / dead next
    
    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    params : Params
      The parameters of the simulation
    
    Returns
    -------
    None
    '''

    # Iterate through all people and find those who are infected
    # Find if they have no time left for disease
    for row, col, personCount in frame.stateGroups[Person.INFECTED.id]:
      person = frame.grid[row][col][personCount]
      if person.framesSinceLastState >= params.INFECTION_PERIOD:
        # Find if the person recovers or dies
        person.framesSinceLastState = 0
        if random() < (params.MORTALITY_RATE * params.COMORBIDITY_COEFFICIENTS[person.age]):
          person.state = Person.DEAD
        else:
          person.state = Person.RECOVERED
  
  @staticmethod
  def findSusceptible(frame, params):
    '''Find out who loses immunity from recovery or vaccination
    
    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    params : Params
      The parameters of the simulation
    
    Returns
    -------
    None
    '''

    # Iterate through all people and find those who are recovered or vaccinated
    # Find if they have lost immunity
    for row, col, personCount in (frame.stateGroups[Person.RECOVERED.id] + 
                                  frame.stateGroups[Person.VACCINATED.id]):
      person = frame.grid[row][col][personCount]
      if person.framesSinceLastState >= params.IMMUNITY_PERIOD:
        # The person loses immunity and becomes susceptible again
        person.state = Person.SUSCEPTIBLE
        person.framesSinceLastState = 0