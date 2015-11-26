from lxml import etree
import re
from pycvnode.connector import *

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
