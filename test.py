from pycvnode import TreeXml

def test(filename):
    t = TreeXml(filename)

    #t.dump()

    c = t.findNode(2).getConnectorByName('ksize')
    c.setValue('(10,10)')

    print t.generate()

if __name__ == '__main__':
    test('tree.xml')
