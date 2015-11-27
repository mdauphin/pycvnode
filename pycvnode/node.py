from lxml import etree
import re
from pycvnode.connector import *

class Node(object):
    def __init__(self, name, connectors = []):
        self.connectors = connectors
        self.name = name
        self.id = 0 #Id load from file
        self.code = None

    def __str__(self):
        return "%s[%d]" % ( self.name, self.id )

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

    def generate_parameters(self, params):
        results = []
        for param in params:
            tmp = param.generate()
            if tmp == None:
                continue
            results.append( tmp )
        return results

    '''remplace in code source variable name by corresponding connector values'''
    def generate(self):
        for i_con in self.getInputConnectors():
            self.code = re.sub( r"\b%s\b" %  i_con.name, i_con.generate(), self.code )
        for o_con in self.getOutputConnectors():
            self.code = re.sub( r"\b%s\b" %  o_con.name, o_con.generate(), self.code )
        return self.code

    '''evaluate python code'''
    def evaluate(self):
        src = self.code
        ns = {}
        #TODO no do in hard codded
        ast = compile( 'import cv2', '<string>', 'exec' )
        exec ast in ns
        print src
        ast = compile( src, '<string>', 'exec' )
        for i_con in self.getInputConnectors():
            ns[ i_con.name ] = i_con.evaluate()
        exec ast in ns
        return ns[self.getOutputConnectors()[0].name]

class NodeXml(Node):
    def __init__(self, filename ):
        tree = etree.parse(filename)
        connector_in = self.loadConnector( tree, "/node/inputs/connector", ConnectorInput )
        connector_out = self.loadConnector( tree, "/node/outputs/connector", ConnectorOutput )
        super( NodeXml, self ).__init__( filename, connectors = connector_in + connector_out )
        self.code = tree.xpath("/node/code")[0].text

    def loadConnector( self, tree, xpath, creator ):
        results = []
        for connector in tree.xpath(xpath):
            connector_name = connector.get('name')
            connector_type = connector.get('type')
            connector_inst = creator(self,connector_name,connector_type)
            results.append( connector_inst )
            setattr( self, connector_name, connector_inst )
        return results
