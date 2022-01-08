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
from math import sqrt, pi
from time import time

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
          self.canvas.arc(person.x * self.canvasWidth, person.y * self.canvasHeight, self.CELL_RADIUS)
          self.canvas.fill_style = person.state.color
          self.canvas.fill()
    
    # Plot the result on the graph
    self.graphXData.append(frameCount)
    currPlot = 0
    for stateID, stateGroup in enumerate(frame.stateGroups):
      state = Person.states[stateID]
      if not state.toGraph:
        # Do not plot this infection state
        continue

      # Add the new data
      self.graphYData[stateID].append(len(stateGroup))
      self.graph.data[currPlot].x.append(frameCount)
      self.graph.data[currPlot].y.append(len(stateGroup))
      currPlot += 1
    
    # Add the hospital capacity data
    if self.params.HOSPITAL_ENABLED:
      self.graph.data[currPlot].x.append(frameCount)
      self.graph.data[currPlot].y.append(
        int(self.params.HOSPITAL_CAPACITY * self.params.POPULATION_SIZE)
      )
      currPlot += 1
      
      self.graph.data[currPlot].x.append(frameCount)
      self.graph.data[currPlot].y.append(
        int(self.params.HOSPITALIZATION_RATE * len(frame.stateGroups[Person.INFECTED.id]))
      )
      currPlot += 1
      
    if self.params.PLOT_EFFECTIVE_REPRODUCTIVE_NUMBER:
      # Add effective reproductive number
      self.graph.data[currPlot].x.append(frameCount)
      self.graph.data[currPlot].y.append(
        max(0.1, frame.effectiveReproductionNumber)
      )
    
    # Render the updates
    self.graph.redraw()
    
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
      
      # Add daily infected and dead counts to the grid
      if Person.INFECTED.toGraph:
        newInfected = (
          self.graphYData[Person.INFECTED.id][-1] - self.graphYData[Person.INFECTED.id][-2]
        )

        self.canvas.fill_text(
          f'Daily Infected: {newInfected}',
          self.canvasWidth - 20 - 50,
          20 + 15
        )
      
      # Add daily infected and dead counts to the grid
      if Person.DEAD.toGraph:
        newDead = self.graphYData[Person.DEAD.id][-1] - self.graphYData[Person.DEAD.id][-2]
      
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
    
    # Set canvas cell render radius
    # The pixel density is the amount of space occupied by one agent if they are uniformly distributed
    # The agent size is 1 / 10 of the pixel density
    pixelDensity = 1 / self.params.POPULATION_SIZE
    cellArea = 0.5 * pixelDensity
    simpleCellRadius = sqrt(cellArea / pi)
    self.CELL_RADIUS = int(min(self.canvasWidth, self.canvasHeight) * simpleCellRadius) 

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
    
    # Set seed to a previous value
    # random.seed(114914)

    # Initialize arrays for graphing the results
    self.graphXData = []
    self.graphYData = [[] for _ in Person.states]

    # Intialize graph
    # Plot the result on the graph
    self.graph.data = []
    for state in Person.states:
      if not state.toGraph:
        # Do not plot this infection state
        continue

      self.graph.data.append(go.Scatter(
        x = [],
        y = [],
        marker = dict(
          color = state.color
        ),
        name = state.name,
        mode = 'lines',
      ))
    
    # Add the hospital capacity line
    if self.params.HOSPITAL_ENABLED:
      self.graph.data.append(go.Scatter(
        x = [],
        y = [],
        marker = dict(
          color = 'orange'
        ),
        name = 'HOSPITAL CAPACITY',
        mode = 'lines',
      ))
      
      self.graph.data.append(go.Scatter(
        x = [],
        y = [],
        marker = dict(
          color = 'black'
        ),
        name = 'HOSPITAL CASES',
        mode = 'lines'
      ))
    
    if self.params.PLOT_EFFECTIVE_REPRODUCTIVE_NUMBER:
      # Plot the effective reproductive number
      self.graph.data.append(go.Scatter(
        x = [],
        y = [],
        marker = dict(
          color = 'purple'
        ),
        name = 'EFFECTIVE REPRODUCTIVE NUMBER',
        mode = 'lines',
        yaxis = 'y2',
      ))

      # Initialize second y axis
      # self.graph.layout.yaxis2.type = 'log'
      self.graph.layout.yaxis2.anchor = 'x'
      self.graph.layout.yaxis2.side = 'right'
      self.graph.layout.yaxis2.showgrid = False
      self.graph.layout.yaxis2.overlaying = 'y'
    
    # Render the graph
    self.graph.layout.yaxis.range = [0, self.params.POPULATION_SIZE]
    self.graph.layout.legend.orientation = 'h'
    self.graph.redraw()
    
    # Set whether vaccinated agents are graphed based on whether it is enabled
    Person.VACCINATED.toGraph = self.params.VACCINATION_ENABLED
    
    # Created a simulation object and runs the simulation
    simulation = Simulation(self.params)
    self.simulationFrames = []
    startTime = time()
    for frameCount, frame in enumerate(simulation.run()):
      self.simulationFrames.append(frame)
      self.drawFrame(frame, frameCount)
      endTime = time()
      sleep(max(0, self.params.TIME_PER_FRAME - (endTime - startTime)))
      startTime = time()
      self.costLabel.text = '; '.join([
        # f'Cost: Rs. {simulation.interventionCost}',
        f'Re: {frame.effectiveReproductionNumber:.2f}',
        f'Td: {frame.doublingTime:.2f}',
        f'Hospital occupancy: {int(frame.hospitalOccupancy * 100)}%',
        # f'Agents contacted: {frame.averageContacts:.2f}',
        f'Peak infection: {frame.peakInfection}'
      ])
    self.interventionCost = simulation.interventionCost
    
    # Add lockdown box
    if self.params.LOCKDOWN_ENABLED:
      # Get the lockdown periods
      lockdownPeriods = []
      curr = False
      for frameCount, lockdown in enumerate(self.params.LOCKDOWN_DAYS):
        if (not curr) and lockdown:
          lockdownPeriods.append([frameCount, 0])
        elif curr and (not lockdown):
          if (frameCount - lockdownPeriods[-1][0]) <= 5:
            lockdownPeriods.pop()
          else:
            lockdownPeriods[-1][1] = frameCount
        curr = lockdown
      print(lockdownPeriods)

      # Create the shapes for display of the lockdown periods
      self.graph.layout.shapes = []
      for startFrame, endFrame in lockdownPeriods:
        self.graph.layout.shapes.append(
          dict(
            type = 'rect',
            xref = 'x',
            yref = 'y',
            x0 = startFrame,
            x1 = endFrame,
            y0 = 0,
            y1 = self.graph.layout.yaxis.range[1],
            fillcolor = 'lightblue',
            opacity = 0.4,
            line = dict(
              color = 'rgb(0, 0, 0, 0)',
              width = 0
            ),
            layer = 'below'
          )
        )
      self.graph.redraw()
    
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
      randomSeed = self.params.RANDOM_SEED
    )
    
    # Downlaod the results as a json file
    # Create BlobMedia object, write json data to it and download the file
    jsonResults = {
      'user': anvil.users.get_user()['email'],
      'params': self.params.__dict__,
      'remarks': self.remarksTextBox.text,
      'simulationData': simulationData,
      'cost': self.interventionCost,
      'time': timeStr,
      'randomSeed': self.params.RANDOM_SEED
    }
    blobMedia = BlobMedia('text', json.dumps(jsonResults).encode('utf-8'), name = f'{timeStr}.json')
    anvil.media.download(blobMedia)
    
    # Disable the save simulation button
    self.saveSimulationButton.enabled = False
