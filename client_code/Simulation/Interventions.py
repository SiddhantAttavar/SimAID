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
    int
      Cost of the vaccinations and hospitalization   in the frame
    '''

    # Iterate through all susceptible people
    # And find out who is vaccinated
    cost = 0
    for row, col, personCount in frame.stateGroups[Person.SUSCEPTIBLE.id]:
      person = frame.grid[row][col][personCount]
      if random() < params.VACCINATION_RATE:
        person.state = Person.VACCINATED
        person.framesSinceLastState = 0
        cost += params.VACCINATION_COST
    
    # Return cost
    return cost
  
  @staticmethod
  def lockdown(frame, frameCount, params, lockdownStrategies):
    '''Find out which cells are under lockdown

    Each cell is under lockdown if its infected population 
    is greater than a certain percentage
    
    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    frameCount : int
      The current frame count of the simulation
    params : Params
      The parameters of the simulation
    lockdownStrategies : Dict[str, func]
      Dictionary of all lockdown strategies
    
    Returns
    -------
    int
      Cost of the lockdown of cells in the frame
    '''

    # For global lockdowns, find if there is a lockdown
    if not params.LOCAL_LOCKDOWN:
      lockdownStrategy = lockdownStrategies[params.LOCKDOWN_STRATEGY]
      lockdownStatus = lockdownStrategy(params, frameCount)
      params.LOCKDOWN_DAYS[frameCount] = lockdownStatus

    # Iterate through all cells and find out which are under lockdown
    cost = 0
    for rowCount, row in enumerate(frame.grid):
      for colCount, cell in enumerate(row):
        # Find the number of infected people in the cell
        infectedCount = 0
        for person in cell:
          infectedCount += person.state == Person.INFECTED
        
        # Check whether the cell should be under lockdown
        if params.LOCAL_LOCKDOWN:
          frame.isLockedDown[rowCount][colCount] = (
            len(cell) > 0 and
            infectedCount / len(cell) >= params.LOCKDOWN_LEVEL
          )
        else:
          frame.isLockedDown[rowCount][colCount] = lockdownStatus

        # Add to the cost if the cell is under lockdown
        if frame.isLockedDown[rowCount][colCount]:
          cost += params.LOCKDOWN_COST * params.RULE_COMPLIANCE_RATE * len(cell)
    
    # Return cost
    return cost
    
  @staticmethod
  def alternatingLockdown(params, frameCount):
    '''Lockdown strategy: Alternating lockdown

    The entire simulation is on lockdown for framesOn frames, 
    and then free to move for framesOff frames, between the [start, stop] range

    Parameters
    ----------
    params : Params
      The parameters of the simulation
    frameCount : int
      The current frame count of the simulation

    Returns
    -------
    bool
      Whether there is a lockdown
    '''

    # Get start, stop values
    start = params.LOCKDOWN_START
    stop = params.LOCKDOWN_STOP
    framesOn = params.ALT_LOCKDOWN_FRAMES_ON
    framesOff = params.ALT_LOCKDOWN_FRAMES_OFF

    # Check if the current frameCount is in the [start, stop] range
    if frameCount < start or stop < frameCount:
      return False
    
    # Check if frameCount is in the lockdown phase
    return (frameCount - start) % (framesOn + framesOff) < framesOn
  
  @staticmethod
  def daysOfWeekLockdown(params, frameCount):
    '''Lockdown strategy: Alternating lockdown

    The entire simulation is on lockdown for certain days of the week
    in a given [start, stop] range, assuming Monday is the first day of the simulation

    Parameters
    ----------
    params : Params
      The parameters of the simulation
    frameCount : int
      The current frame count of the simulation

    Returns
    -------
    bool
      Whether there is a lockdown
    '''

    # Get start, stop values
    start = params.LOCKDOWN_START
    stop = params.LOCKDOWN_STOP

    # Check if the current frameCount is in the [start, stop] range
    if frameCount < start or stop < frameCount:
      return False
    
    # Check if frameCount is in the lockdown day of the week
    day = frameCount % 7
    return params.DAY_LOCKDOWN[day]
    
  @staticmethod
  def blockLockdown(params, frameCount):
    '''Lockdown strategy: Alternating lockdown

    The entire simulation is on lockdown in the [start, stop] range

    Parameters
    ----------
    params : Params
      The parameters of the simulation
    frameCount : int
      The current frame count of the simulation

    Returns
    -------
    bool
      Whether there is a lockdown
    '''

    # Get start, stop values
    start = params.LOCKDOWN_START
    stop = params.LOCKDOWN_STOP

    # Check if the current frameCount is in the [start, stop] range
    return start <= frameCount and frameCount <= stop
