from anvil import server

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
        self.x = Bar.__deserialize__(data['x'], globalData)