#!/usr/bin/python

import operator


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

    def getTopLinks(self, db, vertex, topN):
        neighbors = self.getNeighbors(db, vertex)
        #print neighbors
        neighborOutDegreeDict = {}
        for n in neighbors:
            neighborOutDegreeDict[n] = self.getOutDegree(db, n)
        #print neighborOutDegreeDict
        sortedNeighborOutDegreeDict = sorted(neighborOutDegreeDict.items(), key=operator.itemgetter(1))
        sortedNeighborOutDegreeDict = sortedNeighborOutDegreeDict[-topN:]
        #sortedNeighborOutDegreeDict = reversed(sortedNeighborOutDegreeDict)
        #print sortedNeighborOutDegreeDict
        topNLinks = [i[0] for i in sortedNeighborOutDegreeDict]
        return list(reversed(topNLinks))

    def getCentralGraph(self, db, vertex, topN, depth):
        graph = []
        print "depth = " + str(depth)
        print "vertex = " + vertex
        tempTopLiks = self.getTopLinks(db, vertex, topN)
        print tempTopLiks
        for i in tempTopLiks:
            row = [vertex, i]
            #row.append(vertex)
            #row.append(i)
            graph.append(row)
            if depth > 0:
                nextGraph = self.getCentralGraph(db, i, topN, depth-1)
                for n in nextGraph:
                    graph.append(n)
        return graph

#graphAnalytics = GraphAnalytics()
#db=MySQLdb.connect(host="localhost",user="root", passwd="",db="WikiGraph")
#print graphAnalytics.getTopLinks(db, "'United_States'", 5)
#print graphAnalytics.getCentralGraph(db, "'United_States'", 2, 1)
#print graphAnalytics.getCentralGraph(db, "'Amtrak'", 2, 1)