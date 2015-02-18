#!/usr/bin/python

import json

from flask import Flask, jsonify
from flask_cors import CORS
import MySQLdb

from src.main.analytics.GraphAnalytics import GraphAnalytics


app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods = ['GET'])
def index():
    graphAnalytics = GraphAnalytics()
    db=MySQLdb.connect(host="localhost",user="root", passwd="",db="WikiGraph")
    #graphAnalytics.printDB(db)
    #print getOutDegree(db, "sourceTest")
    #print getInDegree(db, "sourceTest")
    #print getNeighbors(db, "sourceTest")
    neighbors = graphAnalytics.getNeighbors(db, "sourceTest1")
    db.close()
    return jsonify(message=neighbors)

@app.route('/getDB', methods = ['GET'])
def getDB():
    db=MySQLdb.connect(host="localhost",user="root", passwd="",db="WikiGraph")
    cursor=db.cursor()
    cursor.execute("select * from wikiGraph");
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return json.dumps(results)

@app.route('/getPrunedDB', methods = ['GET'])
def getPrunedDB():
    graphAnalytics = GraphAnalytics()
    db=MySQLdb.connect(host="localhost",user="root", passwd="",db="WikiGraph")
    cursor=db.cursor()
    cursor.execute("select * from wikiGraph");
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        outDegree = min(graphAnalytics.getOutDegree(db, row[0]), graphAnalytics.getOutDegree(db, row[1]));
        if outDegree > 500:
            print row[1] + str(outDegree)
        #update to percentile like top 5% instead of a hard coded number for min outDegree
        if(outDegree > 500):
            results.append(dict(zip(columns, row)))
    return json.dumps(results)

#http://localhost:5000/getCentralGraph/'Amtrak'/topN/2/depth/1
@app.route('/getCentralGraph/<vertex>/topN/<int:topN>/depth/<int:depth>', methods = ['GET'])
def getCentralGraph(vertex, topN, depth):
    graphAnalytics = GraphAnalytics()
    db=MySQLdb.connect(host="localhost",user="root", passwd="",db="WikiGraph")
    graph = graphAnalytics.getCentralGraph(db, vertex, topN, depth, [vertex])
    cursor=db.cursor()
    cursor.execute("select * from wikiGraph limit 1");
    columns = [column[0] for column in cursor.description]
    print columns
    results = []
    for row in graph:
        results.append(dict(zip(columns, row)))
    print results
    return json.dumps(results)

if __name__ == '__main__':
    #winreg error on debug=true in python 2.7
    app.run(debug=False)