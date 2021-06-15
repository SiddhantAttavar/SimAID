from ._anvil_designer import RunSimulationTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
from time import sleep

class RunSimulation(RunSimulationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    
  def drawFrame(self, frame):
    print(frame)
    '''This method draws a frame on the canvas'''
    self.canvas.background = 'black'
    
    for person in frame.people:
      self.canvas.arc(person.x, person.y, 5)
      self.canvas.fill_style = 'blue'
      self.canvas.fill()

  def onRunSimulationButtonClick(self, **event_args):
    '''This method is called when the button is clicked'''
    frame = server.call('getFrame')
    #self.drawFrame(frame)
    print(frame.x.x)

@server.portable_class('Bar')
class Bar:
    x = 0

    def __serialize__(self, globalData):
        return {
            'x': self.x
        }
    
    def __deserialize__(self, data, globalData):
        self.__init__()
        self.x = data['x']

@server.portable_class('Foo')
class Foo:
    x = Bar()

    def __serialize__(self, globalData):
        return {
            'x': self.x.__serialize__(globalData)
        }
    
    def __deserialize__(self, data, globalData):
        self.__init__()
        self.x = Bar()
        self.x.__deserialize__(data['x'], globalData)