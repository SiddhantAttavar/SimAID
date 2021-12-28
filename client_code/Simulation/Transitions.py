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

        # Find all susceptible and infected people from the current cell 
        # in the grid and visiting grid
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
        
        # Sort the groups by the x coordinate to implement the two pointer method
        susceptibleGroup.sort(key = lambda person: person.x)
        infectedGroup.sort(key = lambda person: person.x)
        
        # Use the two pointer method to find the exposed agents
        # Maintain two pointers such that all susceptible agents between the two pointers
        # are in the x contact radius of the current infected agent
        leftPointer = 0
        rightPointer = 0
        susceptibleCount = len(susceptibleGroup)

        for infectedPerson in infectedGroup:
          # Move the right pointer to the first susceptible agent 
          # that is not in the x contact radius
          while (rightPointer < susceptibleCount and 
                  susceptibleGroup[rightPointer].x <= infectedPerson.x + params.CONTACT_RADIUS):
            rightPointer += 1
          
          # Similarly, move the left pointer to the first susceptible agent
          # that is in the x contact radius
          while (leftPointer < susceptibleCount and
                  susceptibleGroup[leftPointer].x < infectedPerson.x - params.CONTACT_RADIUS):
            leftPointer += 1
          
          # The infected agent is in contact with 
          # all susceptible agents between the two pointers
          for susceptiblePerson in susceptibleGroup[leftPointer: rightPointer]:
            # Calculate the distance between the two agents to check the y contact radius
            dist = (
              abs(susceptiblePerson.x - infectedPerson.x) ** 2 +
              abs(susceptiblePerson.y - infectedPerson.y) ** 2
            )

            infectionRate = params.INFECTION_RATE
            if (params.HYGIENE_ENABLED and 
                (susceptiblePerson.followsRules and infectedPerson.followsRules)):
              infectionRate *= params.HYGIENE_RATE
            
            # Check for lockdown
            if (frame.isLockedDown[rowCount][colCount] and 
                infectedPerson.followsRules and susceptiblePerson.followsRules):
                continue

            if dist <= params.CONTACT_RADIUS_SQUARED:
              # Increment the agents contacted counter of the infected agent
              infectedPerson.agentsContacted += 1

              if random() < infectionRate:
                # The disease spreads to the susceptible person and he becomes exposed
                susceptiblePerson.state = Person.EXPOSED
                susceptiblePerson.framesSinceLastState = 0
                
                # Increment the agents infected counter of the infected agent
                infectedPerson.agentsInfected += 1

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
        person.agentsInfected = 0
        person.agentsContacted = 0
  
  @staticmethod
  def findRemoved(frame, params):
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
    
    # If no. of hospitalized agents is more than hospital capacity
    # Increase the mortality rate
    numInfected = len(frame.stateGroups[Person.INFECTED.id])
    numHospitalized = int(numInfected * params.HOSPITALIZATION_RATE)
    totalHospitalCapacity = int(params.HOSPITAL_CAPACITY * params.POPULATION_SIZE)
    if numHospitalized > totalHospitalCapacity:
      # If there are x hospitalized people, y is hospital capacity
      # k is the mortality coefficient, and m is the mortality rate then
      # (y + (x - y) * k) / x * m is the new mortality rate
      mortalityRate = params.MORTALITY_RATE * (
        totalHospitalCapacity + 
        (numHospitalized - totalHospitalCapacity) * params.MORTALITY_COEFFICIENT
      ) / numHospitalized
    else:
      mortalityRate = params.MORTALITY_RATE

    # Iterate through all people and find those who are infected
    # Find if they have no time left for disease
    for row, col, personCount in frame.stateGroups[Person.INFECTED.id]:
      person = frame.grid[row][col][personCount]
      if person.framesSinceLastState >= params.INFECTION_PERIOD:
        # Find if the person recovers or dies
        person.framesSinceLastState = 0
        
        # Add to the total agents infected for this frame
        frame.reproductiveSum += person.agentsInfected
        frame.contactSum += person.agentsContacted
        frame.removedAgents += 1
        
        # Find if the person recovers or dies
        if random() < (mortalityRate * params.COMORBIDITY_COEFFICIENTS[person.age]):
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
