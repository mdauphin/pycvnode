from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from pycvnode import TreeXml, NodeHttpRenderer
import os

tree = None

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global tree
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            with open('svg.html') as f:
                self.wfile.write(f.read())
            return
        elif self.path == '/favicon.ico':
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("Not found")
            return
        else:
            filename, file_extension = os.path.splitext(self.path)
            self.send_response(200)
            mime = {
                '.js' : 'application/javascript',
                '.jpg': 'image/jpeg'
            }
            self.send_header('Content-type',mime[file_extension])
            self.end_headers()
            with open(self.path[1:]) as f:
                self.wfile.write(f.read())
            return
            '''
            node_id = int(self.path[1:])
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            contents = NodeHttpRenderer(tree.findNode(node_id)).render()
            self.wfile.write(contents)
            #first_out_con = tree.findNode(node_id).getOutputConnectors()[0]
            #first_out_con.render.render(self)
            '''
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
