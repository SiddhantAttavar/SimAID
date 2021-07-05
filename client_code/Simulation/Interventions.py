from random import random

from Person import Person # type: ignore

class Interventions:
  """This class contains the functions for the intervention strategies

  Attributes
  ----------

  Methods
  -------
  vaccinate(frame, params)
    Find out who is vaccinated
  """

  @staticmethod
  def vaccinate(frame, params):
    """"Find out who is vaccinated

    Parameters
    ----------
    frame : Frame
      The current frame of the simulation
    
    Returns
    -------
    None
    """

    for personCount in frame.stateGroups[Person.SUSCEPTIBLE.id]:
      person = frame.people[personCount]
      if random() < params.VACCINATION_RATE:
        person.state = Person.VACCINATED