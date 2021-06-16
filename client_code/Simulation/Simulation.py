from random import random, randint

from Frame import Frame # type: ignore
from Person import Person # type: ignore

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
        self.simulationLength = 50

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
            person.state = Person.states[randint(0, 5)]

        for frameCount in range(self.simulationLength):
            # For each frame of the simulation, 
            # we need to randomly place each person in the grid
            for person in self.population:
                person.x = random()
                person.y = random()
            
            # Then we need to build the Frame object to yield
            currFrame = Frame(self.population)
            yield currFrame

if __name__ == '__main__':
    # Only performed when this file is run directly
    from matplotlib import pyplot as plt

    def drawFramesMatplotlib(frames):
        """Draws the frame in a matplotlib graph.

        Parameters
        ----------
        frame : list(Frame)
            The list of frames that we have to display
        frameCount : int
            The current frameCount
        
        Returns
        -------
        None
        """

        # Initialize arrays for graphing the results
        graphXData = []
        graphYData = [[] for _ in Person.states]

        # Get the data for the X and Y axes
        for frameCount, frame in enumerate(frames):
            graphXData.append(frameCount + 1)
            for stateID, stateCount in enumerate(frame.stateCounts):
                graphYData[stateID].append(stateCount)
        
        # Add the plots to the graph
        for stateID, stateCountData in enumerate(graphYData):
            plt.plot(
                graphXData,
                stateCountData,
                label = Person.states[stateID].name,
                color = Person.states[stateID].color
            )
        
        # Show the matplotlib plots
        plt.show()

    # Created a simulation object and runs the simulation
    simulation = Simulation()
    frames = list(simulation.run())
    drawFramesMatplotlib(frames)