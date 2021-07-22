import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from random import random

from Person import Person # type: ignore

class Interventions:
  '''This class contains the functions for the intervention strategies

  Attributes
  ----------

  Methods
  -------
  vaccinate(frame, params)
    Finds out who is vaccinated
  lockdown(frame, params)
    Lockdown cells in the grid
  '''

  @staticmethod
  def vaccinate(frame, params):
    '''Find out who is vaccinated

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

    # Iterate through all susceptible people
    # And find out who is vaccinated
    for row, col, personCount in frame.stateGroups[Person.SUSCEPTIBLE.id]:
      person = frame.grid[row][col][personCount]
      if random() < params.VACCINATION_RATE:
        person.state = Person.VACCINATED
        person.framesSinceLastState = 0
  
  @staticmethod
  def lockdown(frame, params):
    '''Find out which cells are under lockdown
    
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

    # Iterate through all cells and find out which are under lockdown
    for rowCount, row in enumerate(frame.grid):
      for colCount, cell in enumerate(row):
        # Find the number of infected people in the cell
        infectedCount = 0
        for person in cell:
          infectedCount += person.state == Person.INFECTED
        
        # Check whether the cell should be under lockdown
        frame.isLockedDown[rowCount][colCount] = (len(cell) > 0 and 
                                                  infectedCount / len(cell) >= params.LOCKDOWN_LEVEL)