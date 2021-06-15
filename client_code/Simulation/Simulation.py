from .Frame import Frame
from .Person import Person

def getFrame():
    """Get a frame from anvil"""
    return Frame([Person(50, 50)])