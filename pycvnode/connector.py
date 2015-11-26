class Connector(object):

    class Direction:
        OUTPUT = 1
        INPUT  = 2

    def __init__(self,name,direction):
        self.name = name
        self.direction = direction
        self.value = None
        self.parser = None

    def setValue(self,value):
        self.value = self.parser.parse(value)

    def evaluate(self):
        return None

class ConnectorInput(Connector):

    def __init__(self,name):
        self.connection = None
        super( ConnectorInput, self ).__init__( name, Connector.Direction.INPUT );

    def evaluate(self):
        if self.connection != None:
            return self.connection.output_connector.evaluate()
        if self.value != None:
            if isinstance(self.value, str):
                return "'%s'" % self.value
            return str(self.value)

class ConnectorOutput(Connector):
    _cpt = 0

    def __init__(self,name):
        self.varname = self.generate_uniq_var()
        self.connections = []
        super( ConnectorOutput, self ).__init__( name, Connector.Direction.OUTPUT )

    def generate_uniq_var(self):
        ConnectorOutput._cpt += 1
        return "var%d" % ( ConnectorOutput._cpt )

    def evaluate(self):
        return self.varname

class ConnectorParser(object):
    def __init__(self,type):
        self.type = type
        self.converter = {
            'str' : self.toStr,
            'int' : self.toInt,
            'float' : self.toFloat,
            'tuple' : self.toTuple,
             }
    def parse(self,value):
        return self.converter[self.type](value)
    def toStr(self,value):
        return value
    def toInt(self,value):
        return int(value)
    def toFloat(self,value):
        return foat(value)
    def toTuple(self,value):
        return eval(value)
