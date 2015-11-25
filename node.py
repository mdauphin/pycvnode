from lxml import etree
import re

class Node(object):
    def __init__(self, function_name, connectors = []):
        self.connectors = connectors
        self.function_name = function_name
        self.id = 0 #Id load from file

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

    def findNode( self, id ):
        results = [ x for x in self.nodes if x.id == id ]
        if len(results)>0:
            return results[0]
        return None

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

class Connection(object):
    def __init__(self,ouput_connector,input_connector):
        self.output_connector = ouput_connector
        self.input_connector = input_connector

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
            connector_type = connector.get('type')
            connector_inst = creator(connector_name)
            connector_inst.parser = ConnectorParser(connector_type)
            results.append( connector_inst )
            setattr( self, connector_name, connector_inst )
        return results

    def generate(self):
        for i_con in self.getInputConnectors():
            self.code = re.sub( r"\b%s\b" %  i_con.name, i_con.evaluate(), self.code )
        for o_con in self.getOutputConnectors():
            self.code = re.sub( r"\b%s\b" %  o_con.name, o_con.evaluate(), self.code )
        return self.code


def test(filename):
    t = Tree()

    tree = etree.parse(filename)

    for xml_node in tree.xpath('/tree/node'):
        node = NodeXml(xml_node.get('name') + '.xml' )
        setattr( node, 'id', xml_node.get('id'))
        t.nodes.append(node)
        for xml_param in xml_node.findall('param'):
            connector = node.getConnectorByName(xml_param.get('name'))
            connector.setValue( xml_param.get('value') )

    for xml_connection in tree.xpath('/tree/connections/connection'):
        xml_src = xml_connection.find('src')
        src = t.findNode( xml_src.get('id') )
        xml_dst = xml_connection.find('dst')
        dst = t.findNode( xml_dst.get('id') )
        t.connect( src.getConnectorByName(xml_src.get('name')),
        dst.getConnectorByName(xml_dst.get('name')) )

    t.generate()

if __name__ == '__main__':
    test('tree.xml')
