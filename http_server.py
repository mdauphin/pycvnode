from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from pycvnode import TreeXml

tree = None

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global tree
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<p>hello</p>')
            self.wfile.write('</body></html>')
            return
        else:
            node_id = int(self.path[1:])
            first_out_con = tree.findNode(node_id).getOutputConnectors()[0]
            first_out_con.render.render(self)
            return

def main(filename):
    try:
        global tree
        tree = TreeXml(filename)
        server = HTTPServer(('',8080),HttpHandler)
        print "Server http://localhost:8080/"
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main('tree.xml')
