#!/usr/bin/python

import MySQLdb

class GraphAnalytics:  

    def printDB(self, db):
        print "Printing DB:"
        c=db.cursor()
        c.execute("select * from wikiGraph")
        dict = c.fetchall()
        for i in dict:
            print i
        return
    
    def getOutDegree(self, db, source):
        c=db.cursor()
        c.execute("select count(*) from wikiGraph where source = %s", (source,))
        dict = c.fetchall()
        return dict[0][0]
    
    def getInDegree(self, db, destination):
        c=db.cursor()
        c.execute("select count(*) from wikiGraph where destination = %s", (destination,))
        dict = c.fetchall()
        return dict[0][0]
    
    def getNeighbors(self, db, vertex):
        c=db.cursor()
        c.execute("select destination from wikiGraph where source = %s", (vertex,))
        dict = c.fetchall()
        neighborList = []
        for i in dict:
            neighborList.append(i[0])
        return neighborList
