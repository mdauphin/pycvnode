from pycvnode.connection import Connection
from pycvnode.node import NodeXml
from lxml import etree

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
        results = "import cv2\n"
        for node in self.nodes:
            results += node.generate() + "\n"
        return results

    def findNode( self, id ):
        results = [ x for x in self.nodes if x.id == id ]
        if len(results)>0:
            return results[0]
        raise Exception('Tree','No node with id = %d' % id )

    def dump(self):
        for node in self.nodes:
            print node

class TreeXml(Tree):
    def __init__(self,filename):
        super( TreeXml, self ).__init__()

        tree = etree.parse(filename)

        for xml_node in tree.xpath('/tree/node'):
            node = NodeXml(xml_node.get('name') + '.xml' )
            setattr( node, 'id', int(xml_node.get('id')))
            self.nodes.append(node)
            for xml_param in xml_node.findall('param'):
                connector = node.getConnectorByName(xml_param.get('name'))
                connector.setValue( xml_param.get('value') )

        for xml_connection in tree.xpath('/tree/connections/connection'):
            xml_src = xml_connection.find('src')
            src = self.findNode( int(xml_src.get('id')) )
            xml_dst = xml_connection.find('dst')
            dst = self.findNode( int(xml_dst.get('id')) )
            self.connect( src.getConnectorByName(xml_src.get('name')),
            dst.getConnectorByName(xml_dst.get('name')) )
