#!/usr/bin/python
import random
import threading

import MySQLdb

from src.main.scraper.Producer import Producer


class MainDriver:

    def __init__(self, maxProducers):
        self.maxProducers = maxProducers

    def run(self):
        producerThreads = []
        producerId = 0;
        for i in xrange(self.maxProducers):
            producerThreads.append(ProducerThread(Producer(), producerId))
            producerId += 1
        for i in producerThreads:
            i.start()

class ProducerThread(threading.Thread):
    def __init__(self, producer, threadID):
        threading.Thread.__init__(self)
        self.producer = producer
        self.threadID = threadID

    def run(self):
        print "Starting " + str(self.threadID)
        while True:
            self.producer.produceLinks(self.getRandomPage())
        print "Ending " + str(self.threadID)

    def getRandomPage(self):
        db=MySQLdb.connect(host="localhost",user="root", passwd="",db="WikiGraph")
        c=db.cursor()
        c.execute("select destination from wikiGraph")
        dict = c.fetchall()
        destinationList = []
        for i in dict:
            destinationList.append(i[0])
        db.close()
        #note the [1:-1] strips the quotes around the string that get added from the db query
        return random.choice(destinationList)[1:-1]


mainDriver = MainDriver(10)
#db=MySQLdb.connect(host="localhost",user="root", passwd="",db="WikiGraph")
#print mainDriver.getRandomPage(db)
mainDriver.run()