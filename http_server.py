from flask import Flask, jsonify, redirect, Response
from pycvnode import TreeXml, ConnectorRenderer, TreeJson
import os

app = Flask(__name__)

tree = None

@app.route("/")
def index():
    return redirect("http://localhost:5000/static/svg.html", code=302)

@app.route("/config")
def config():
    json = TreeJson(tree).render()
    return jsonify(**json)

@app.route("/image/<int:node_id>")
def image(node_id):
    node = tree.findNode(node_id)
    data = ConnectorRenderer(node.getOutputConnectors()[0]).render()
    return Response(data, mimetype='image/png')


if __name__ == '__main__':
    filename = 'tree.xml'
    tree = TreeXml(filename)
    app.debug = True
    app.run()
