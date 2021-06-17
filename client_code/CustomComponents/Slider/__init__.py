from anvil import *

class Slider(SliderTemplate):
  def __init__(self, **properties):
    self._shown = False
    
    # You must call self.init_components() before doing anything else in this function
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.
    
  @property
  def level(self):
    return self._level
  
  @level.setter
  def level(self, value):
    self._level = value
    self.update()
    
  @property
  def slider_min(self):
    return self._slider_min
  
  @slider_min.setter
  def slider_min(self, value):
    self._slider_min = value
    self.update()
    
  @property
  def slider_max(self):
    return self._slider_max
  
  @slider_max.setter
  def slider_max(self, value):
    self._slider_max = value
    self.update()
    
  @property
  def step(self):
    return self._step
  
  @step.setter
  def step(self, value):
    self._step = value
    self.update()
    
  @property
  def level(self):
    return self._level
  
  @level.setter
  def level(self, value):
    self._level = value
    self.update()
    
  def slider_change(self, value, **event_args):
    self._level = int(value)
    self.raise_event("change", level=self.level)
  
  def update(self):
    if self._shown:
      self.call_js('set_behavior', self.level, self.slider_min, self.slider_max, self.step)

  
  def form_show(self, **event_args):
    """This method is called when the HTML panel is shown on the screen"""
    self._shown = True
    self.update()
