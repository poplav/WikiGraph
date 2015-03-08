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