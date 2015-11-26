import cv2

class Connector(object):

    class Direction:
        OUTPUT = 1
        INPUT  = 2

    def __init__(self,node,name,direction,type):
        self.node = node
        self.name = name
        self.direction = direction
        self.value = None
        self.type = type
        self.parser = ConnectorParser(self)
        self.render = ConnectorRenderer(self)

    def setValue(self,value):
        self.value = self.parser.parse(value)

    def generate(self):
        return None

    def evaluate(self):
        raise Exception('Connector','Can not evaluate generic Connector')

class ConnectorInput(Connector):

    def __init__(self,node,name,type):
        self.connection = None
        super( ConnectorInput, self ).__init__( node, name,
         Connector.Direction.INPUT, type );

    def generate(self):
        if self.connection != None:
            return self.connection.output_connector.generate()
        if self.value != None:
            if isinstance(self.value, str):
                return "'%s'" % self.value
            return str(self.value)

    def evaluate(self):
        if self.connection != None:
            return self.connection.output_connector.eval()
        elif self.value != None:
            return self.value
        else:
            raise Exception('ConnectorInput','No connection no value to evaluate')

class ConnectorOutput(Connector):
    _cpt = 0

    def __init__(self,node,name,type):
        self.varname = self.generate_uniq_var()
        self.connections = []
        super( ConnectorOutput, self ).__init__( node, name,
         Connector.Direction.OUTPUT, type )

    def generate_uniq_var(self):
        ConnectorOutput._cpt += 1
        return "var%d" % ( ConnectorOutput._cpt )

    def generate(self):
        return self.varname

    def evaluate(self):
        return self.node.evaluate()


class ConnectorParser(object):
    def __init__(self,connector):
        self.connector = connector
        self.converter = {
            'str' : self.toStr,
            'int' : self.toInt,
            'float' : self.toFloat,
            'tuple' : self.toTuple,
             }
    def parse(self,value):
        return self.converter[self.connector.type](value)
    def toStr(self,value):
        return value
    def toInt(self,value):
        return int(value)
    def toFloat(self,value):
        return foat(value)
    def toTuple(self,value):
        return eval(value)

class ConnectorRenderer(object):
    def __init__(self,connector):
        self.connector = connector
        self.converter = {
            'str' : self.toStr,
            'int' : self.toStr,
            'float' : self.toStr,
            'tuple' : self.toStr,
            'numpy.ndarray' : self.toImg,
             }
    def render(self, http):
        return self.converter[self.connector.type](http,self.connector.evaluate())

    def toImg(self, http, value ):
        http.send_response(200)
        http.send_header('Content-type','image/png')
        http.end_headers()
        http.wfile.write(cv2.imencode( '.png', value  ))

    def toStr(self,value):
        http.send_response(200)
        http.send_header('Content-type','text/html')
        http.end_headers()
        http.wfile.write('<p>%s</p>' % value)
        return
