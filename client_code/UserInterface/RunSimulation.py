from ._anvil_designer import RunSimulationTemplate # type: ignore
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
from plotly import graph_objects as go
from time import sleep
from datetime import datetime
import json
import random

from ..Simulation.Simulation import Simulation
from ..Simulation.Person import Person
from ..Simulation.Params import Params

class RunSimulation(RunSimulationTemplate):
  '''Class which changes the UI in the RunSimulation form.
  
  Attributes
  ----------
  canvasWidth : int
    The width of the canvas
  canvasHeight : int
    The height of the canvas
  timePerFrame : float
    The number of second each frame is displayed for
  graphXData : List[int]
    The data in the X axis of the graph
  graphYData : List[Tuple[int]]
    The data in the Y axis of the graph
  params : Params
    The parameters of the simulation
  interventionCost : int
    The cost of the interntion measures in the simulation

  Methods
  -------
  __init__(**properties)
    Initializes the run simulation form
  drawFrame(frame)
    Draws a frame on the UI
  '''

  def __init__(self, params = Params(), **properties):
    '''Initializes the run simulation page
    
    Called when the RunSimulation form is created.
    Sets Form properties and Data Bindings and then
    runs any other code for initializing the form.

    Parameters
    ----------
    params : Params
      The parameters of the simulation
    **properties : dict
      The UI properties of the form
    
    Returns
    -------
    None
    '''
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.
    self.params = params
    
  def drawFrame(self, frame, frameCount):
    '''This method draws a frame on the canvas.
    
    For each frame, we are doing 2 things
    The first task is to draw each person in the frame 
    on the grid, in its appropriate color
    The second task is to plot the total number of people
    from each compartment on the graph in their respective colors

    Parameters
    ----------
    frame
      The frame to draw
    frameCount
      The current frame count in the simulation
    
    Returns
    -------
    None
    '''
    
    # Initialize the canvas with a black, empty background
    self.canvas.clear_rect(0, 0, self.canvasWidth, self.canvasHeight)
    
    # Draw the boxes for the cells
    # First draw the rows
    self.canvas.begin_path()
    for rowCount in range(self.params.GRID_SIZE):
      self.canvas.move_to(0, rowCount * self.params.CELL_SIZE * self.canvasHeight)
      self.canvas.line_to(self.canvasWidth, rowCount * self.params.CELL_SIZE * self.canvasHeight)
    self.canvas.move_to(0, self.canvasHeight)
    self.canvas.line_to(self.canvasWidth, self.canvasHeight)
    
    # Then draw the columns
    for colCount in range(self.params.GRID_SIZE):
      self.canvas.move_to(colCount * self.params.CELL_SIZE * self.canvasWidth, 0)
      self.canvas.line_to(colCount * self.params.CELL_SIZE * self.canvasWidth, self.canvasHeight)
    self.canvas.move_to(self.canvasWidth, 0)
    self.canvas.line_to(self.canvasWidth, self.canvasHeight)

    # Commit the changes to the canvas
    self.canvas.stroke_style = "#2196F3"
    self.canvas.line_width = 3
    self.canvas.stroke()
    
    # Draw each person on the canvas as a dot with a particular color
    for rowCount, row in enumerate(frame.grid):
      for colCount, cell in enumerate(row):
        # If the cell is locked down, shade it gray
        if frame.isLockedDown[rowCount][colCount]:
          self.canvas.fill_style = 'grey'
          self.canvas.fill_rect(
            colCount * self.params.CELL_SIZE * self.canvasWidth, 
            rowCount * self.params.CELL_SIZE * self.canvasHeight, 
            self.params.CELL_SIZE * self.canvasWidth, 
            self.params.CELL_SIZE * self.canvasHeight
          )
        
        for person in cell:
          self.canvas.begin_path()
          self.canvas.arc(person.x * self.canvasWidth, person.y * self.canvasHeight, 5)
          self.canvas.fill_style = person.state.color
          self.canvas.fill()
    
    # Plot the result on the graph
    self.graphXData.append(frameCount)
    self.graph.data = []
    for stateID, stateGroup in enumerate(frame.stateGroups):
      if stateID == Person.VACCINATED.id and not self.params.VACCINATION_ENABLED:
        # No need to show vaccination group if vaccination is not enabled
        continue

      self.graphYData[stateID].append(len(stateGroup))
      figure = go.Scatter(
        x = self.graphXData,
        y = self.graphYData[stateID],
        marker = dict(
          color = Person.states[stateID].color
        ),
        name = Person.states[stateID].name
      )
      self.graph.data.append(figure)
    
    # Add the hospital capacity line
    self.graph.data.append(go.Scatter(
      x = self.graphXData,
      y = [int(self.params.HOSPITAL_CAPACITY * self.params.POPULATION_SIZE) 
            for _ in range(self.params.SIMULATION_LENGTH)],
      marker = dict(
        color = 'orange'
      ),
      name = 'HOSPITAL_CAPACITY'
    ))
    
    self.graph.data = self.graph.data
    
    # Draw a box for the daily counts in the corner
    if frameCount > 0:
      self.canvas.fill_style = 'blue'
      self.canvas.stroke_style = 'white'
      self.canvas.fill_rect(self.canvasWidth - 20 - 100, 20, 100, 40)
      self.canvas.stroke_rect(self.canvasWidth - 20 - 100, 20, 100, 40)
      self.canvas.fill()
      self.canvas.stroke()
      
      self.canvas.line_width = 1
      self.canvas.fill_style = 'white'
      self.canvas.font = '12px montserrat'
      self.canvas.text_align = 'center'
      self.canvas.text_baseline = 'center'
      
      newInfected = self.graphYData[Person.INFECTED.id][-1] - self.graphYData[Person.INFECTED.id][-2]
      newDead = self.graphYData[Person.DEAD.id][-1] - self.graphYData[Person.DEAD.id][-2]
      self.canvas.fill_text(
        f'Daily Infected: {newInfected}',
        self.canvasWidth - 20 - 50,
        20 + 15
      )
      self.canvas.fill_text(
        f'Daily Dead: {newDead}',
        self.canvasWidth - 20 - 50,
        20 + 30
      )
      
      self.canvas.fill()
      
  def onCanvasShow(self, **event_args):
    '''This method is called when the Canvas is shown on the screen
    
    Initializes the canvas dimensions
    
    Parameters
    ----------
    **event_args
      Details of the canvas
    
    Returns
    -------
    None
    '''
    
    self.canvasWidth = self.canvas.get_width()
    self.canvasHeight = self.canvas.get_height()
    self.canvas.background = 'black'

  def onRunSimulationButtonClick(self, **event_args):
    '''This method is called when the run simulation button is clicked
    
    Parameters
    ----------
    **event_args
      Details about how the button is clicked
    
    Returns
    -------
    None
    '''
    
    # Initalize and save seed
    startTime = datetime.now()
    self.randomSeed = startTime.hour * 10000 + startTime.minute * 100 + startTime.second
    random.seed(self.randomSeed)
    
    # Set seed to a previous value
    #random.seed(114914)

    # Initialize arrays for graphing the results
    self.graphXData = []
    self.graphYData = [[] for _ in Person.states]
    
    # Created a simulation object and runs the simulation
    simulation = Simulation(self.params)
    self.simulationFrames = []
    for frameCount, frame in enumerate(simulation.run()):
      self.simulationFrames.append(frame)
      self.drawFrame(frame, frameCount)
      sleep(self.params.TIME_PER_FRAME)
      self.costLabel.text = f'Cost: Rs. {simulation.interventionCost}'
    self.interventionCost = simulation.interventionCost
    
    # Once the simulation is over, allow the user to save it
    if anvil.users.get_user() is not None:
      self.saveSimulationButton.enabled = True

  def onSaveSimulationButtonClick(self, **event_args):
    '''This method is called when the save simulation button is clicked
    
    Parameters
    ----------
    **event_args
      Details about how the button is clicked
    
    Returns
    -------
    None
    '''

    # Check if the user is signed in
    if anvil.users.get_user() is None:
      return
    
    # Get current time
    time = datetime.now()
    timeStr = time.strftime("%m/%d/%Y, %H:%M:%S")

    # Get simulation data
    stateNames = [state.name for state in Person.states]
    simulationData = dict(zip(stateNames, self.graphYData))
    print(simulationData)
    
    # Save the simulation to the database
    # user: the email of the user
    # params: rhe simulation parameters as a python dictionary
    # remarks: user remarks
    # simulationData: results of the simulation
    # cost: cost of the simulation in INR
    row = app_tables.simulations.add_row(
      user = anvil.users.get_user()['email'],
      params = self.params.__dict__,
      remarks = self.remarksTextBox.text,
      simulationData = simulationData,
      cost = self.interventionCost,
      time = time,
      randomSeed = self.randomSeed
    )
    
    # Downlaod the results as a json file
    # Create BlobMedia object, write json data to it and download the file
    jsonResults = {
      'user': anvil.users.get_user()['email'],
      'params': self.params.__dict__,
      'simulationData': simulationData,
      'cost': self.interventionCost,
      'time': timeStr,
      'randomSeed': self.randomSeed
    }
    blobMedia = BlobMedia('text', json.dumps(jsonResults).encode('utf-8'), name = f'{timeStr}.json')
    anvil.media.download(blobMedia)
    
    # Disable the save simulation button
    self.saveSimulationButton.enabled = False