#!/usr/bin/python

import pika

class Consumer:
    
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='graph')
        self.done = True
        
    def __del__(self):
        self.connection.close()
        
    def consumeLinks(self):
         self.channel.basic_consume(self.callback, queue='graph', no_ack=True)
         self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print " [x] Received %r" % (body,)
    
consumer = Consumer()
consumer.consumeLinks()