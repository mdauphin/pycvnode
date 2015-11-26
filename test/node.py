import unittest
from pycvnode import Node, ConnectorInput, ConnectorOutput
import numpy as np
'''
to run this test
python -m unittest test.node
to run all test
python -m unittest discover
see http://stackoverflow.com/a/24266885/2137364
'''

class TestNode(unittest.TestCase):

    def testEvaluate(self):
        ci = ConnectorInput(None,'ci','str')
        ci.setValue('Hello')
        co = ConnectorOutput(None,'co', 'str')

        n = Node('name', [ ci, co ])
        co.node = n
        n.code = 'co = ci + " World"'

        self.assertEqual( n.evaluate(), 'Hello World' )

    def testNumpy(self):
        ci = ConnectorInput(None,'ci','numpy.ndarray')
        ci.value = np.zeros([3,3])
        co = ConnectorOutput(None,'co', 'numpy.ndarray')

        n = Node('name', [ ci, co ])
        co.node = n
        n.code = 'co = ci + 1'

        self.assertTrue( np.array_equal( n.evaluate(), np.ones([3,3]) ) )

    def testOpencv(self):
        ci = ConnectorInput( None, 'filename', 'str')
        ci.value = 'file.png'
        co = ConnectorOutput( None, 'im', 'numpy.ndarray')

        n = Node('name', [ ci, co ])
        co.node = n
        n.code = 'im = cv2.imread( filename, 0)'

        ret = n.evaluate()

        self.assertTrue( np.array_equal( ret.shape, (99, 82) ) )

if __name__ == '__main__':
    unittest.main()
