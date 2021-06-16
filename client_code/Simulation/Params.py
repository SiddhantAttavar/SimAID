class Params:
    """Parameters for the simulation.
    
    Simulation Parameters
    ---------------------
    POPULATION_SIZE
        The size of the population in the simulation
    SIMULATION_LENGTH
        The number of frams in the simulation
    CONTACT_RADIUS : float
        The maximum distance between two individuals who are in contact
    INFECTION_RATE : float
        The chance of an infected person infecting a suseptible person
    INFECTION_PERIOD : int
        The duration for which an infected person has the disease
    MORTALITY_RATE : float
        The chance of an infected person dying
    INITIAL_INFECTED : int
        The number of people who are infected at the beginning
    """

    POPULATION_SIZE = 100
    SIMULATION_LENGTH = 50
    CONTACT_RADIUS = 0.1
    INFECTION_RATE = 0.6
    INFECTION_PERIOD = 10
    MORTALITY_RATE = 0.3
    INITIAL_INFECTED = 2

    def __init__(self, **kwargs):
        """Initializes the parameters.

        Parameters
        ----------
        **kwargs
            Arguments to change the default parameters
        
        Returns
        -------
        None
        """

        # Change the value for each parameter in kwargs from default
        for param, value in kwargs.items():
            exec(f'{param} = {value}')