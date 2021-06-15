from anvil import server

class Person:
    """Store variables and methods for Person.

    The person class is used to store variables
    and methods for each person / agent
    This includes properties like position, infection status,
    comorbidities, etc. and functions like move etc.

    Attributes
    ----------
    x : int
        An integer which stores the X-coordinate of the person
    y : int
        An integer which stores the Y-coordinate of the person
    state : State
        A variable which stores the current state of the person

    Methods
    -------
    
    Classes
    -------
    State
        An enum which stores the different states a person can have
    """

    class State:
        """Enum which contains various states of the disease
        
        The disease states are:
            SUSCEPTIBLE - The person can contract the disease
            EXPOSED - The person has contracted the disease but is asymptomatic
            INFECTED - The person has contracted the disease and is symptomatic
            RECOVERED - The person no longer has the disease and is immune
            DEAD - The person has died from the disease
            VACCINATED - The person has been vaccinated and is immune
        """

        SUSCEPTIBLE = '0'
        EXPOSED = '1'
        INFECTED = '2'
        RECOVERED = '3'
        DEAD = '4'
        VACCINATED = '5'

        states = [
            SUSCEPTIBLE,
            EXPOSED,
            INFECTED,
            RECOVERED,
            DEAD,
            VACCINATED
        ]

    def __init__(self, startX, startY):
        """Set some initial parameters for the person.

        Parameters
        ----------
        startX : int
            The starting X coordinate
        startY : int
            The starting Y coordinate
        """

        self.x = startX
        self.y = startY
        self.state = Person.State.SUSCEPTIBLE