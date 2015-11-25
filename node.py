from lxml import etree
import re

class Node(object):
    def __init__(self, function_name, connectors = []):
        self.connectors = connectors
        self.function_name = function_name

    def getConnectorByName( self, name ):
        matches = [ x for x in self.connectors if x.name == name ]
        if len(matches) != 1:
            return None
        return matches[0]

    def getConnectors(self, direction):
        return [ x for x in self.connectors if x.direction == direction ]

    def getInputConnectors(self):
        return self.getConnectors( Connector.Direction.INPUT )

    def getOutputConnectors(self):
        return self.getConnectors( Connector.Direction.OUTPUT )

    def generate(self):
        return None

    def eval_parameters(self, params):
        results = []
        for param in params:
            tmp = param.evaluate()
            if tmp == None:
                continue
            results.append( tmp )
        return results

    def function_call(self, ret, params):
        function_name = 'cv2.%s' % self.function_name
        return "%s = %s( %s )" % ( ret, function_name, ','.join( self.eval_parameters(params) ) )

class Tree(object):
    def __init__(self, nodes = [], connections = []):
        self.nodes = nodes
        self.connections = connections

    def connect( self, connector_out, connector_in ):
        connection = Connection( connector_out, connector_in )
        self.connections.append( connection )
        connector_out.connections.append( connection )
        connector_in.connection = connection

    def generate(self):
        print "import cv2"
        for node in self.nodes:
            print node.generate()

class Connector(object):

    class Direction:
        OUTPUT = 1
        INPUT  = 2

    def __init__(self,name,direction):
        self.name = name
        self.direction = direction
        self.value = None

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

class Connection(object):
    def __init__(self,ouput_connector,input_connector):
        self.output_connector = ouput_connector
        self.input_connector = input_connector

class NodeImRead(Node):
    def __init__(self):
        self.filename = ConnectorInput("filename")
        self.flags = ConnectorInput("flags")
        self.im = ConnectorOutput("im")
        super( NodeImRead, self ).__init__( "imread", connectors = [ self.filename, self.flags, self.im ] )

    def generate(self):
        return self.function_call( self.im.varname, [self.filename, self.flags] )

class NodeImWrite(Node):
    def __init__(self):
        self.filename = ConnectorInput("filename")
        self.img = ConnectorInput("img")
        self.params = ConnectorInput("params")
        self.retval = ConnectorOutput("retval")
        super( NodeImWrite, self ).__init__( "imwrite", connectors = [ self.filename, self.img, self.params, self.retval ] )


    def generate(self):
        return self.function_call( self.retval.varname, [self.filename, self.img, self.params] )

class NodeBlur(Node):

    def __init__(self):
        self.src = ConnectorInput("src")
        self.ksize = ConnectorInput("ksize")
        self.dst = ConnectorOutput("dst")
        super( NodeBlur, self ).__init__( "blur", connectors = [ self.src, self.ksize, self.dst ] )

    def generate(self):
        return self.function_call( self.dst.varname, [self.src, self.ksize] )

class NodeXml(Node):
    def __init__(self, filename ):
        tree = etree.parse(filename)
        connector_in = self.loadConnector( tree, "/node/inputs/connector", ConnectorInput )
        connector_out = self.loadConnector( tree, "/node/outputs/connector", ConnectorOutput )
        self.code = tree.xpath("/node/code")[0].text
        super( NodeXml, self ).__init__( "imread", connectors = connector_in + connector_out )

    def loadConnector( self, tree, xpath, creator ):
        results = []
        for connector in tree.xpath(xpath):
            connector_name = connector.get('name')
            connector_inst = creator(connector_name)
            results.append( connector_inst )
            setattr( self, connector_name, connector_inst )
        return results

    def generate(self):
        for i_con in self.getInputConnectors():
            self.code = re.sub( r"\b%s\b" %  i_con.name, i_con.evaluate(), self.code )
        for o_con in self.getOutputConnectors():
            self.code = re.sub( r"\b%s\b" %  o_con.name, o_con.evaluate(), self.code )
        return self.code

def test():
    t = Tree()

    n1 = NodeXml(filename = 'nodes/imread.xml')
    n1.filename.value = "file.png"
    n1.flags.value = 1

    n2 = NodeBlur()
    n2.src = n1.im
    n2.ksize.value = (3,3)

    n3 = NodeImWrite()
    n3.filename.value = "output.png"


    t.nodes.append(n1)
    t.nodes.append(n2)
    t.nodes.append(n3)

    t.connect( n1.getConnectorByName('im'), n2.getConnectorByName('src') )
    t.connect( n2.getConnectorByName('dst'), n3.getConnectorByName('img') )


    t.generate()

if __name__ == '__main__':
    test()
