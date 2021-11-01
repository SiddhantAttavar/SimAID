from ._anvil_designer import MainTemplate # type: ignore
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.users

from .RunSimulation import RunSimulation
from .SimulationControls import SimulationControls

class Main(MainTemplate):
  '''Class which changes the UI in the main page
  
  Attributes
  ----------
  
  Methods
  -------
  __init__(**properties)
    Initializes the main page
  '''

  def __init__(self, **properties):
    '''Initializes the main page
    
    Parameters
    ----------
    **properties : dict
      The UI properties of the page
    
    Returns
    -------
    None
    '''

    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.simulationControlsForm = SimulationControls()
    self.root.add_component(self.simulationControlsForm, full_width_row = True)		
    
    if anvil.users.get_user() is None:
      self.signInButton.text = 'Login / Signup'
    else:
      self.signInButton.text = 'Logout'

  def onSimulationControlsLinkClick(self, **event_args):
    '''This method is called when the simulation controls link in the navbar is clicked
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''

    self.root.clear()
    self.root.add_component(self.simulationControlsForm, full_width_row = True)

  def onRunSimulationLinkClick(self, **event_args):
    '''This method is called when the simulation link in the navbar is clicked
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''

    self.root.clear()
    self.root.add_component(RunSimulation(params = self.simulationControlsForm.params), full_width_row = True)

  def onSignInClick(self, **event_args):
    '''This method is called when the sign in button is clicked
    
    Parameters
    ----------
    **event_args
      Details about how the slider is moved
    
    Returns
    -------
    None
    '''

    if anvil.users.get_user() is None:
      # We have to login the user
      anvil.users.login_with_form()
      
      if anvil.users.get_user() is not None:
        # The user is now logged in
        self.signInButton.text = 'Logout'
    else:
      # The user is logged in and we have to log the user out
      anvil.users.logout()
      self.signInButton.text = 'Login / Signup'
