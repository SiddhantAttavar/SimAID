from random import random
from math import sqrt

from Frame import Frame # type: ignore
from Person import Person # type: ignore
from Params import Params # type: ignore

class Simulation:
    """Parameters and methods for the simulation.

    Attributes
    ----------
    self.PARAMS : Params
        The parameters of the simulation

    Methods
    -------
    __init__()
        Initialized the simulation with some properties
    run()
        Runs the current simulation
    """

    def __init__(self, PARAMS):
        """"Initialized the simulation

        Intializes the simulation with some basic properties

        Parameters
        ----------
        PARAMS : Params
            The parameters of the simulation

        Returns
        -------
        None
        """

        self.PARAMS = PARAMS

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

        # Create the first frame
        # Intialize the population list with people
        people = [Person(0, 0) for _ in range(self.PARAMS.POPULATION_SIZE)]
        for person in people:
            person.x = random()
            person.y = random()
            person.state = Person.SUSCEPTIBLE

        # There are some people who are infected at the beginning
        for infectedCount in range(self.PARAMS.INITIAL_INFECTED):
            people[infectedCount].state = Person.INFECTED
            people[infectedCount].framesSinceInfection = 0

        currFrame = Frame(people)
        print(currFrame.stateCounts)
        yield currFrame

        for frameCount in range(self.PARAMS.SIMULATION_LENGTH):
            # Then we need to build the Frame object to yield
            currFrame = self.nextFrame(currFrame)
            yield currFrame

    def nextFrame(self, frame):
        """Calculate the next frame of the simulation.

        Parameters
        ----------
        frame : Frame
            The current frame of the simulation

        Returns
        -------
        Frame
            The next frame of the simulation
        """

        frame = self.findInfected(frame)
        frame = self.findRecovered(frame)

        return frame

    def findInfected(self, frame):
        """Find out who will be infected next
        
        Parameters
        ----------
        frame : Frame
            The current frame of the simulation
        
        Returns
        -------
        Frame
            The frame after some people have been infected
        """

        # Find the people who are susceptible and infected
        suseptibleGroup = []
        infectedGroup = []
        for person in frame.people:
            if person.state == Person.SUSCEPTIBLE:
                suseptibleGroup.append(person)
            elif person.state == Person.INFECTED:
                infectedGroup.append(person)
        
        # Find if any of the two groups are in contact and the disease spreads
        for infectedPerson in infectedGroup:
            for susceptiblePerson in suseptibleGroup:
                dist = sqrt(
                    abs(infectedPerson.x - susceptiblePerson.x) ** 2 + 
                    abs(infectedPerson.y - susceptiblePerson.y) ** 2
                )
                if dist <= self.PARAMS.CONTACT_RADIUS and random() < self.PARAMS.INFECTION_RATE:
                    # The disease spreads to the susceptible person
                    susceptiblePerson.state = Person.INFECTED
                    susceptiblePerson.framesSinceInfection = 0
                    frame.stateCounts[Person.SUSCEPTIBLE.id] -= 1
                    frame.stateCounts[Person.INFECTED.id] += 1
        
        return frame
    
    def findRecovered(self, frame):
        """Find out who will be recovered / dead next
        
        Parameters
        ----------
        frame : Frame
            The current frame of the simulation
        
        Returns
        -------
        Frame
            The frame after some people have been recovered / dead
        """

        # Iterate through all people and find those who are infected
        # Find if they have no time left for disease
        for person in frame.people:
            if person.state == Person.INFECTED:
                person.framesSinceInfection += 1
                if person.framesSinceInfection >= self.PARAMS.INFECTION_PERIOD:
                    # Find if the person recovers or dies
                    person.framesSinceInfection = -1
                    frame.stateCounts[Person.INFECTED.id] -= 1
                    if random() < self.PARAMS.MORTALITY_RATE:
                        person.state = Person.DEAD
                        frame.stateCounts[Person.DEAD.id] += 1
                    else:
                        person.state = Person.RECOVERED
                        frame.stateCounts[Person.RECOVERED.id] += 1
        
        return Frame(frame.people)

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
            graphXData.append(frameCount)
            for stateID, stateCount in enumerate(frame.stateCounts):
                graphYData[stateID].append(stateCount)

        # Add the plots to the graph
        for stateID, stateCountData in enumerate(graphYData):
            plt.plot(
                graphXData,
                stateCountData,
                label = Person.states[stateID].name,
                color = Person.states[stateID].color,
            )

        # Show the matplotlib plots
        plt.ylim(0, 100)
        plt.show()

    # Created a simulation object and runs the simulation
    params = Params()
    simulation = Simulation(params)
    frames = list(simulation.run())
    drawFramesMatplotlib(frames)