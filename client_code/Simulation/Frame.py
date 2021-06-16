from .Person import Person

class Frame:
    """Stores information about each frame in the simulation.

    Attributes
    ----------
    people : list(Person.State)
        list of people in the population
    stateCounts : list(int)
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
        self.stateCounts = [0 for _ in Person.states]

        # Iterate through the list and increment the state count
        for person in self.people:
            self.stateCounts[person.state.id] += 1