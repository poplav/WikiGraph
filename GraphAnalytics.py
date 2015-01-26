#!/usr/bin/python

import MySQLdb

def printDB(db):
    print "Printing DB:"
    c=db.cursor()
    c.execute("select * from wikiGraph")
    dict = c.fetchall()
    for i in dict:
        print i
    return

def getOutDegree(db, source):
    c=db.cursor()
    c.execute("select count(*) from wikiGraph where source = %s", (source,))
    dict = c.fetchall()
    return dict[0][0]

def getInDegree(db, destination):
    c=db.cursor()
    c.execute("select count(*) from wikiGraph where destination = %s", (destination,))
    dict = c.fetchall()
    return dict[0][0]

def getNeighbors(db, vertex):
    c=db.cursor()
    c.execute("select destination from wikiGraph where source = %s", (vertex,))
    dict = c.fetchall()
    neighborList = []
    for i in dict:
        neighborList.append(i[0])
    return neighborList

db=MySQLdb.connect(host="localhost",user="root", passwd="",db="graph")
printDB(db)
print getOutDegree(db, "sourceTest")
print getInDegree(db, "sourceTest")
print getNeighbors(db, "sourceTest")
db.close()
