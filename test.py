from pycvnode import *
from lxml import etree

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
