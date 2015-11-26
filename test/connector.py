import unittest
from pycvnode import ConnectorInput

'''
to run this test
python -m unittest test.connector
to run all test
python -m unittest discover
see http://stackoverflow.com/a/24266885/2137364
'''

class TestConnector(unittest.TestCase):

    def testConnectorInputStr(self):
        c = ConnectorInput(None,'name','str')
        c.setValue('Hello')
        r = c.evaluate()
        self.assertEqual( r, 'Hello' )
        self.assertTrue( isinstance(r,str)  )

    def testConnectorInputTuple(self):
        c = ConnectorInput(None,'name','tuple')
        c.setValue('(1,2,3)')
        r = c.evaluate()
        self.assertEqual( r, (1,2,3) )
        self.assertTrue( isinstance(r,tuple)  )

if __name__ == '__main__':
    unittest.main()
