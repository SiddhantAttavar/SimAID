from anvil import server
from enum import Enum

class Person:
    """Stores variables and methods for Person.

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
    __init__()
        Initializes the person object with some properties

    Enums
    -----
    State
        The state of the person
    """

    class State(Enum):
        """Enum which contains various states of the disease and their colors.
        
        STATES
        ------
            SUSCEPTIBLE : The person can contract the disease
            EXPOSED : The person has contracted the disease but is asymptomatic
            INFECTED : The person has contracted the disease and is symptomatic
            RECOVERED - The person no longer has the disease and is immune
            DEAD - The person has died from the disease
            VACCINATED - The person has been vaccinated and is immune
        """

        SUSCEPTIBLE = 'green'
        EXPOSED = 'orange'
        INFECTED = 'red'
        RECOVERED = 'blue'
        DEAD = 'gray'
        VACCINATED = 'yellow'

    def __init__(self, startX, startY):
        """Sets some initial parameters for the person.

        Parameters
        ----------
        startX : int
            The starting X coordinate
        startY : int
            The starting Y coordinate
        
        Returns
        -------
        None
        """

        self.x = startX
        self.y = startY
        self.state = Person.State.SUSCEPTIBLE