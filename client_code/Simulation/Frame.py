from .Person import Person

class Frame:
    """Stores information about each frame in the simulation.

    Attributes
    ----------
    people : list(Person.State)
        list of people in the population
    stateCounts : dict(Person.State, int)
        A count of number of people in each state

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

        # Initialize the variables and set every state in Person.State to 0
        self.people = people
        self.stateCounts = []

        for state in Person.states:
            self.stateCounts[state.id] = 0

        # Iterate through the list and increment the state count
        for person in self.people:
            self.stateCounts[person.state.id] += 1