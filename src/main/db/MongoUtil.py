#!/usr/bin/python

from pymongo import MongoClient

class MongoUtil:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client["wikiGraph"]
        self.collection = self.db["vertices"]

    def createUniqueIndex(self):
        self.collection.create_index("name", unique=True, background=True, safe=True)

    def removeAllDocuments(self):
        self.collection.remove({})

    def insertVertex(self, vertexName):
        vertex = {"name":vertexName, "neighbors":[]}
        self.collection.insert(vertex)

    #***FIX***Note efficient and should be unique neighbors
    def addNeighbor(self, vertexName, neighborName):
        id = mu.getVertexByName(vertexName)["_id"]
        neighborCursor = mu.getVertexByName(vertexName)["neighbors"]
        neighborList = []
        for i in neighborCursor:
            neighborList.append(i)
        neighborList.append(neighborName)
        neighborDict = {}
        neighborDict["neighbors"] = neighborList
        mu.updateNeighbors(id, neighborDict)

    def updateNeighbors(self, id, neighborList):
        self.collection.update({"_id":id}, {"$set":neighborList}, upsert=False)

    def getVertexByName(self, vertexName):
        return self.collection.find_one({"name":vertexName})

    def printCollection(self):
        for i in self.collection.find():
            print i

mu = MongoUtil()
usa = "United_States"
mu.removeAllDocuments()
#mu.createUniqueIndex()
mu.insertVertex(usa)
mu.printCollection()
mu.addNeighbor(usa, "a")
mu.printCollection()