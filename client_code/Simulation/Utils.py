import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from random import random
from bisect import bisect_left as insertLeft

from Person import Person # type: ignore

class Utils:
  '''This class contains utility functions
  
  Attributes
  ----------

  Methods
  -------
  drawFramesMatplotlib(frames, params)
    Creates a matplotlib graph and displays it locally
  getRandomCell(params)
    Gets a random cell from the grid
  '''
  
  @staticmethod
  def drawFramesMatplotlib(frames, params):
    '''Draws the frame in a matplotlib graph.

    Parameters
    ----------
    frame : list(Frame)
      The list of frames that we have to display
    frameCount : int
      The current frameCount
    params : Params
      The parameters of the simulation

    Returns
    -------
    None
    '''
    
    # Import matplotlib
    from matplotlib import pyplot as plt

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
    plt.ylim(0, params.POPULATION_SIZE)
    plt.show()

  @staticmethod
  def getRandomCell(params, probabilities):
    '''Generates a random cell in the grid

    Parameters
    ----------
    params : Params   
      The parameters of the simulation
    Probabilities
      The list of probabilities to choose a cell from
    
    Returns
    -------
    cellRow : int
      The row of the generated cell
    cellCol : int
      The column of the generated cell
    '''

    cellNum = insertLeft(params.GRID_PROBABILITIES, random())
    cellRow = cellNum // params.GRID_SIZE
    cellCol = cellNum % params.GRID_SIZE

    return cellRow, cellCol