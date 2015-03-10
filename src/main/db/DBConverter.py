#!/usr/bin/python

from MongoUtil import MongoUtil
from MySQLUtil import MySQLUtil
import MySQLdb

class DBConverter:

    def convertMySQLToMongo(self, MySQLdb):
        mongodb = MongoUtil()
        cursor=MySQLdb.cursor()
        cursor.execute("select * from wikiGraph")
        for row in cursor:
            mongodb.insertVertex(row[0])
            mongodb.addNeighbor(row[0], row[1])

converter = DBConverter()
converter.convertMySQLToMongo(MySQLUtil().db)