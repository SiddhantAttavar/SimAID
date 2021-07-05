from time import time
from matplotlib import pyplot as plt

from Person import Person # type: ignore
from Params import Params # type: ignore

class Utils:
  """This class contains utility functions
  
  Attributes
  ----------

  Methods
  -------
  drawFramesMatplotlib()
    Creates a matplotlib graph and displays it locally
  """
  
  @staticmethod
  def drawFramesMatplotlib(frames, params):
    """Draws the frame in a matplotlib graph.

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
    plt.ylim(0, params.POPULATION_SIZE)
    plt.show()