#!/usr/bin/python

import pika
import MySQLdb

class Consumer:
    
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='graph')
        self.done = True
        self.db=MySQLdb.connect(host="localhost",user="root", passwd="",db="WikiGraph")
        
    def __del__(self):
        self.connection.close()
        
    def consumeLinks(self):
         self.channel.basic_consume(self.callback, queue='graph', no_ack=True)
         self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print " [x] Received %r" % (body,)
        row = body.split( );
        cursor=self.db.cursor()
        print row
        try:
            cursor.execute("insert into wikiGraph values(\"%s\", \"%s\")", (row[0],row[2]))
        except:
            print "duplicate entry skipping"
        self.db.commit()
    
consumer = Consumer()
consumer.consumeLinks()