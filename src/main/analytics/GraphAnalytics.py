#!/usr/bin/python

import operator
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

    def getTopLinks(self, db, vertex, topN):
        neighbors = self.getNeighbors(db, vertex)
        #print neighbors
        neighborOutDegreeDict = {}
        for n in neighbors:
            neighborOutDegreeDict[n] = self.getOutDegree(db, n)
        #print neighborOutDegreeDict
        sortedNeighborOutDegreeDict = sorted(neighborOutDegreeDict.items(), key=operator.itemgetter(1))
        #print sortedNeighborOutDegreeDict
        sortedNeighborOutDegreeDict = sortedNeighborOutDegreeDict[-topN:]
        #sortedNeighborOutDegreeDict = reversed(sortedNeighborOutDegreeDict)
        #print sortedNeighborOutDegreeDict
        topNLinks = [i[0] for i in sortedNeighborOutDegreeDict]
        return list(reversed(topNLinks))

    def getTopLinksNotInPrevLinks(self, db, vertex, topN, prevLinks):
        neighbors = self.getNeighbors(db, vertex)
        #print neighbors
        print prevLinks
        neighborOutDegreeDict = {}
        for n in neighbors:
            found = False
            for i in prevLinks:
                if n == i:
                    found = True
                    print "found!"
                    break
            if not found:
                neighborOutDegreeDict[n] = self.getOutDegree(db, n)
        #print neighborOutDegreeDict
        sortedNeighborOutDegreeDict = sorted(neighborOutDegreeDict.items(), key=operator.itemgetter(1))
        #print sortedNeighborOutDegreeDict
        sortedNeighborOutDegreeDict = sortedNeighborOutDegreeDict[-topN:]
        #sortedNeighborOutDegreeDict = reversed(sortedNeighborOutDegreeDict)
        #print sortedNeighborOutDegreeDict
        topNLinks = [i[0] for i in sortedNeighborOutDegreeDict]
        return list(reversed(topNLinks))

    def getCentralGraph(self, db, vertex, topN, depth, prevLinks):
        graph = []
        print "depth = " + str(depth)
        print "vertex = " + vertex
        #tempTopLinks = self.getTopLinks(db, vertex, topN)
        tempTopLinks = self.getTopLinksNotInPrevLinks(db, vertex, topN, prevLinks)
        prevLinks += tempTopLinks
        #print prevLinks
        print tempTopLinks
        for i in tempTopLinks:
            row = [vertex, i]
            #row.append(vertex)
            #row.append(i)
            graph.append(row)
            if depth > 0:
                nextGraph = self.getCentralGraph(db, i, topN, depth-1, prevLinks)
                for n in nextGraph:
                    graph.append(n)
        return graph

    def getOutDegreeDistribution(self, db):
        vertices = []
        verticesCountDict = {}
        c = db.cursor()
        c.execute("select distinct source from wikiGraph")
        dict = c.fetchall()
        for i in dict:
            vertices.append(i[0])
        #print vertices
        #print len(vertices)
        for i in vertices:
            verticesCountDict[i] = self.getOutDegree(db, i)
        #print len(verticesCountDict)
        return verticesCountDict

#graphAnalytics = GraphAnalytics()
#db=MySQLdb.connect(host="localhost",user="root", passwd="",db="WikiGraph")
#print graphAnalytics.getOutDegreeDistribution(db)
#print graphAnalytics.getTopLinks(db, "'United_States'", 5)
#print graphAnalytics.getCentralGraph(db, "'United_States'", 2, 1)
#print graphAnalytics.getCentralGraph(db, "'Amtrak'", 2, 1)