from flask import Flask, jsonify
from pycvnode import TreeXml, NodeHttpRenderer, TreeJson
import os

app = Flask(__name__)

tree = None

@app.route("/config")
def config():
    json = TreeJson(tree).render()
    return jsonify(**json)

if __name__ == '__main__':
    filename = 'tree.xml'
    tree = TreeXml(filename)
    app.debug = True
    app.run()
