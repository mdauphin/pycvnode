from pycvnode import TreeXml

def test(filename):
    t = TreeXml(filename)

    print t.generate()

if __name__ == '__main__':
    test('tree.xml')
