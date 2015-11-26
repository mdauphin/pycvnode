from pycvnode import TreeXml

def test(filename):
    t = TreeXml(filename)

    #t.dump()

    c = t.findNode(2).getConnectorByName('ksize')
    c.setValue('(10,10)')

    ns = { 'b' : 2 }
    src = 'a = 1 + b'
    ast = compile( src, '<string>', 'exec' )
    exec ast in ns
    print ns['a']

    #print t.generate()

if __name__ == '__main__':
    test('tree.xml')
