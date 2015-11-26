from pycvnode.connection import Connection

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
