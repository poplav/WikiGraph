#!/usr/bin/python

import urllib2
from sets import Set

class PageParser:

    def __init__(self, channel):
        self.channel = channel

    def getLinks(self, page):
        goodLinks = Set([])
        badLinks = Set([])
        
        response = urllib2.urlopen("http://en.wikipedia.org/wiki/" + page)
        html = response.read()
        wikiLink = "href=\"/wiki/"
        
        indexLocation = html.index(wikiLink)
        pageLinks = []
        while 1==1:
            try:
                indexLocation = html.index(wikiLink, indexLocation+5)
                titleLocation = html.index("title", indexLocation)
                #print html[indexLocation+12:titleLocation-2]
                pageLinks.append(html[indexLocation+12:titleLocation-2])
            except:
                break
        
        print "pageLinks size = " + str(len(pageLinks))
        count = 0
        for link in pageLinks:
            completeUrl = "http://en.wikipedia.org/wiki/" + link
            if completeUrl in goodLinks or completeUrl in badLinks:
                continue
            if self.validUrl(completeUrl):
                goodLinks.add(completeUrl)
                self.channel.basic_publish(exchange='', routing_key='graph', body=page + " -> " +link)
                print "[x] Sent: " + page + " -> " +link
            else:
                badLinks.add(completeUrl)
            count+=1
            print count
            
        
        print "Good Link size = " + str(len(goodLinks))
        print "Bad Link size = " + str(len(badLinks))
        return goodLinks

    def validUrl(self, link):
        try:
            urllib2.urlopen(link)
            return True
        except urllib2.HTTPError, e:
            #print(e.code)
            return False
        except urllib2.URLError, e:
            #print(e.args)
            return False

#PP = PageParser()
#print PP.getLinks("United_States")