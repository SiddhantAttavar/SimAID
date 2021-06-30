from Person import Person # type: ignore

class Frame:
  """Stores information about each frame in the simulation.

  Attributes
  ----------
  people : list(Person.State)
    list of people in the population
  stateGroupss : list(list(int))
    list of indexes of the people in each states

  Methods
  -------
  __init__(people)
    Initializes the Frame object with some properties
  """

  def __init__(self, people):
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
    self.people = people
    self.stateGroups = [[] for _ in Person.states]

    # Iterate through the list and add the person to the state group
    for personCount, person in enumerate(self.people):
      self.stateGroups[person.state.id].append(personCount)