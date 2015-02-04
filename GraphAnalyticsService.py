#!/usr/bin/python

from flask import Flask, jsonify
from flask_cors import CORS
import MySQLdb
from GraphAnalytics import GraphAnalytics

app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods = ['GET'])
def index():
    graphAnalytics = GraphAnalytics()
    db=MySQLdb.connect(host="localhost",user="root", passwd="",db="graph")
    #printDB(db)
    #print getOutDegree(db, "sourceTest")
    #print getInDegree(db, "sourceTest")
    #print getNeighbors(db, "sourceTest")
    neighbors = graphAnalytics.getNeighbors(db, "sourceTest")
    db.close()
    return jsonify(message=neighbors)

if __name__ == '__main__':
    app.run(debug=True)