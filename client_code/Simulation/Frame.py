from .Person import Person

class Frame:
    """Store information about each frame in the simulation.

    Attributes
    ----------
    people : list(Person.State)
        list of people in the population
    stateCounts : dict(Person.State, int)
        A count of number of people in each state
    """

    def __init__(self, people):
        """Set some initial parameters for the frame.
        
        Parameters
        ----------
        people : list(Person.State)
            list of people in the population in the current frame
        """

        # Initialize the variables and set every state in Person.State to 0
        self.people = people
        self.stateCounts = {}

        for state in Person.State.states:
            self.stateCounts[state] = 0

        # Iterate through the list and increment the state count
        for person in self.people:
            self.stateCounts[person.state] += 1
        
    def __serialize__(self, global_data):
        """Serialize the data of the frame to send to anvil"""
        return {
            'people': [person.__serialize__('') for person in self.people],
            'stateCounts': self.stateCounts
        }

    def __deserialize__(self, data, globalData):
        """Deserialize the data of the frame to initialize the object"""
        self.__init__([Person.__deserialize__(person, '') for person in data['people']],)
        self.stateCounts = data['stateCounts']