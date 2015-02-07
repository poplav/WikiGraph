#!/usr/bin/python

import pika
from PageParser import PageParser

class Producer:
    
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='graph')
        self.done = True
        
    def __del__(self):
        self.connection.close()
        
    def produceLinks(self, page):
        self.done = False
        PP = PageParser(self.channel)
        links = PP.getLinks(page)
        #for i in links:
        #    self.channel.basic_publish(exchange='', routing_key='graph', body=i)
        #    print "[x] Sent: " + i
        self.done = True
        return
    
producer = Producer()
producer.produceLinks("United_States")