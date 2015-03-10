#!/usr/bin/python

from pymongo import MongoClient
from DBUtil import DBUtil

class MongoUtil(DBUtil):

    def __init__(self):
        self.initDB()

    def initDB(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client["wikiGraph"]
        self.collection = self.db["vertices"]

    def createUniqueIndex(self):
        self.collection.create_index("name", unique=True, background=True, safe=True)

    def removeAllDocuments(self):
        self.collection.remove({})

    def insertVertex(self, vertexName):
        try:
            vertex = {"name":vertexName, "neighbors":[]}
            self.collection.insert(vertex)
        except:
            print "Vertex " + vertexName + " already exists"

    def addNeighbor(self, vertexName, neighborName):
        id = mu.getVertexByName(vertexName)["_id"]
        neighborDict = {}
        neighborDict["neighbors"] = neighborName
        self.collection.update({"_id":id}, {"$addToSet":neighborDict}, upsert=True)

    # #***FIX***Not efficient and should be unique neighbors
    # def addNeighbor(self, vertexName, neighborName):
    #     id = mu.getVertexByName(vertexName)["_id"]
    #     neighborCursor = mu.getVertexByName(vertexName)["neighbors"]
    #     neighborList = []
    #     for i in neighborCursor:
    #         if neighborName == i:
    #             return
    #         neighborList.append(i)
    #     neighborList.append(neighborName)
    #     neighborDict = {}
    #     neighborDict["neighbors"] = neighborList
    #     mu.updateNeighbors(id, neighborDict)
    #
    # def updateNeighbors(self, id, neighborList):
    #     self.collection.update({"_id":id}, {"$set":neighborList}, upsert=False)

    def getOutDegree(self, vertexName):
        return len(self.getVertexByName(vertexName)["neighbors"])

    def getNeighbors(self, vertexName):
            return self.getVertexByName(vertexName)["neighbors"]

    def getVertexByName(self, vertexName):
        return self.collection.find_one({"name":vertexName})

    def printCollection(self):
        for i in self.collection.find():
            print i

mu = MongoUtil()
usa = "'United_States'"
#mu.removeAllDocuments()
#mu.createUniqueIndex()
mu.insertVertex(usa)
#mu.printCollection()
print mu.getOutDegree(usa)
mu.addNeighbor(usa, "a")
mu.addNeighbor(usa, "a")
#mu.printCollection()
print mu.getOutDegree(usa)
mu.insertVertex(usa)
print mu.getNeighbors(usa)
#
# dbUtil = MongoUtil()
# dbUtil.initDB()
# print dbUtil.getNeighbors(usa)