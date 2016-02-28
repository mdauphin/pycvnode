class Connection(object):
    def __init__(self,ouput_connector,input_connector):
        self.output_connector = ouput_connector
        self.input_connector = input_connector

class ConnectionJson(object):
    """docstring for ConnectionJson"""
    def __init__(self, connection):
        super(ConnectionJson, self).__init__()
        self.connection = connection

    def render(self):
        #{ 'src' : { 'id' : 1, 'name' : 'conOut' }, 'dst' : { 'id' : 2, 'name' : 'conIn'} },
        return {
            'src' : {
                'id' : self.connection.output_connector.node.id,
                'name' : self.connection.output_connector.node.name
                },
            'dst' : {
                'id' : self.connection.output_connector.node.id,
                'name' : self.connection.output_connector.node.name,
            }
        }
