from Person import Person # type: ignore

class Frame:
  """Stores information about each frame in the simulation.

  Attributes
  ----------
  grid : list(list(list(Person)))
    list of people in each cell of the grid
  stateGroupss : list(list(int))
    list of indexes of the people in each states

  Methods
  -------
  __init__(people)
    Initializes the Frame object with some properties
  """

  def __init__(self, grid, params):
    """Sets some initial parameters for the frame.
    
    Parameters
    ----------
    people : list(Person.State)
      list of people in the population in the current frame
    
    Returns
    -------
    None
    """

    # Initialize the variables and set every state in Person.State to an empty list
    self.grid = grid
    self.stateGroups = [[] for _ in Person.states]

    # Iterate through the list and add the person to the state group
    for row in range(params.GRID_SIZE):
      for col in range(params.GRID_SIZE):
        for personCount, person in enumerate(self.grid[row][col]):
          self.stateGroups[person.state.id].append((row, col, personCount))