from ._anvil_designer import MySimulationsTemplate # type: ignore
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from plotly import graph_objects as go

class MySimulations(MySimulationsTemplate):
  '''Class which changes the UI in the MySimulations form
  
  Attributes
  ----------

  Methods
  -------
  __init__(**properties)
    Initializes the run simulation form
  addRow(row)
    Adds a row to the my simulation page
  '''

  def __init__(self, **properties):
    '''Initializes the my simulations page
    
    Parameters
    ----------
    **properties : dict
      The UI properties of the form
    
    Returns
    -------
    None
    '''

    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    # We need to get the saved simulations from the user and display them
    for row in app_tables.simulations.get(user = anvil.user.get_user()):
      self.addRow(row)
  
  def addRow(self, row):
    '''Adds a row to the my simulations page
    
    Parameters
    ----------
    row : dict
      The row from the simulation table
    
    Returns
    -------
    None
    '''

    # Create a new graph and label to add to the page
    graph = Graph()
    label = Label(text = '')

    # Get the data from the database
    graphXData = list(range(len(row['simulation_data'][0])))

    def onClick(self, **event_args):
      ''''Called when the text is clicked'''