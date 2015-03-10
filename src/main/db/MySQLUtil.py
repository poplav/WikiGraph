#!/usr/bin/python

import operator
import MySQLdb
from DBUtil import DBUtil

class MySQLUtil(DBUtil):

    def __init__(self):
        self.initDB()

    def initDB(self):
        self.db=MySQLdb.connect(host="localhost",user="root", passwd="",db="WikiGraph")

    def getNeighbors(self, vertexName):
        c=self.db.cursor()
        c.execute("select destination from wikiGraph where source = %s", (vertexName,))
        dict = c.fetchall()
        neighborList = []
        for i in dict:
            neighborList.append(i[0])
        return neighborList

    def getOutDegree(self, vertexName):
        return

    def addNeighbor(self, vertexName, neighborName):
        return

    def insertVertex(self, vertexName):
        return