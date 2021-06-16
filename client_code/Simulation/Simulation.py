from random import random

from .Frame import Frame
from .Person import Person

class Simulation:
    """Parameters and methods for the simulation.
    
    Attributes
    ----------
    populationSize : int
        The population size of the simulation (default is 0)
    population : list(Person)
        The list of individuals in the simulation
    simulationLength
        The number of frames that the simulation will run for

    Methods
    -------
    __init__()
        Initialized the simulation with some properties
    run()
        Runs the current simulation
    """

    def __init__(self):
        """"Initialized the simulation
        
        Intializes the simulation with some basic properties

        Parameters
        ----------
        dimensions
            Dimensions of the simulation grid

        Returns
        -------
        None
        """

        self.populationSize = 100
        self.simulationLength = 10

    def run(self):
        """Run the simulation.
        
        Run an agent based simulation based on the 
        configuration of the current simulation.

        Parameters
        ----------
            
        Yields
        ------
        Frame
            Constantly yields frames of simulation as they are calculated
        
        Returns
        -------
        None
        """

        # Intialize the population list with people
        self.population = [Person(0, 0) for _ in range(self.populationSize)]
        for person in self.population:
            person.state = Person.SUSCEPTIBLE

        for frameCount in range(self.simulationLength):
            # For each frame of the simulation, 
            # we need to randomly place each person in the grid
            for person in self.population:
                person.x = random()
                person.y = random()
            
            # Then we need to build the Frame object to yield
            currFrame = Frame(self.population)
            yield currFrame