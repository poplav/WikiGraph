WikiGraph Project
======

Populate wiki graph in mysql using RabbitMQ and run some queries on it for now

Testing graph service with d3, sample screen shots:
![Alt text](/screenshots/centralGraphAmtrak.png?raw=true "Central Graph of Amtrak")
---
![Alt text](/screenshots/initUSACrawl.png?raw=true "Init USA crawl Test")
---
![Alt text](/screenshots/graphTest.png?raw=true "Init Graph Test")
---
Provide a central view of a vertex out to some depth with links to the top N neighbors where the neighbors are sorted by out degree<br/>
def getCentralGraph(self, db, vertex, topN, depth):<br/>
print graphAnalytics.getCentralGraph(db, "'Amtrak'", 2, 1)
---
depth = 1  <br/>
vertex = 'Amtrak' <br/>
["'Canada'", "'South_Dakota'"]<br/>
depth = 0<br/>
vertex = 'Canada'<br/>
["'National_Hockey_League'", "'North_America'"]<br/>
depth = 0<br/>
vertex = 'South_Dakota'<br/>
["'Iraq_War'", "'Nevada'"]<br/>
[["'Amtrak'", "'Canada'"], ["'Canada'", "'National_Hockey_League'"], ["'Canada'", "'North_America'"], ["'Amtrak'", "'South_Dakota'"], ["'South_Dakota'", "'Iraq_War'"], ["'South_Dakota'", "'Nevada'"]]
