class Node(object):
	def __init__(self, inputs = [], outputs = []):
		self.inputs = inputs
		self.outputs = outputs

class Connector(object):

	class Direction:
		OUTPUT = 1
		INPUT  = 2

	def __init__(self,name,direction):
		self.name = name
		self.direction = direction

class ConnectorInput(Connector):
	def __init__(self,name):
		super( ConnectorInput, self ).__init__( name, Connector.Direction.INPUT );

class ConnectorOutput(Connector):
	def __init__(self,name):
		super( ConnectorOutput, self ).__init__( name, Connector.Direction.OUTPUT );

class Connection(object):
	def __init__(self,ouput_connector,input_connector):
		self.output_connector = ouput_connector
		self.input_connector = input_connector

class NodeImRead(Node):
	def __init__(self):
		super( NodeImRead, self ).__init__( inputs = [ ConnectorInput("filename"), ConnectorInput("flags") ], outputs = [ ConnectorOutput("im") ] )

class NodeBlur(Node):
	def __init__(self):
		super( NodeBlur, self ).__init__( inputs = [ ConnectorInput("src"), ConnectorInput("kernel") ], outputs = [ ConnectorOutput("dst") ] )

def test():
	v = Connector.Direction.INPUT
	n = NodeImRead()
	n2 = NodeBlur()

if __name__ == '__main__':
	test()
