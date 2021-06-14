from anvil import server

# Contains the skeleton of the Frame Class

@server.portable_class('Frame')
class Frame:
  
  # Methods
  def __init__(self, people):
    pass

@server.portable_class('Person')
class Person():
  pass

@server.portable_class('State')
class State():
  pass