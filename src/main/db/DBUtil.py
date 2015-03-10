#!/usr/bin/python

import abc

class DBUtil(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def initDB(self):
        return

    @abc.abstractmethod
    def getNeighbors(self, vertex):
        return

    @abc.abstractmethod
    def getOutDegree(self, vertexName):
        return

    @abc.abstractmethod
    def addNeighbor(self, vertexName, neighborName):
        return

    @abc.abstractmethod
    def insertVertex(self, vertexName):
        return