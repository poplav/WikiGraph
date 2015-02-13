WikiGraph Project
======

Populate wiki graph in mysql using RabbitMQ and run some queries on it for now

Testing graph service with d3, sample screen shots:
![Alt text](/screenshots/initUSACrawl.png?raw=true "Init USA crawl Test")
![Alt text](/screenshots/graphTest.png?raw=true "Init Graph Test")

Provide a central view of a vertex out to some depth with links to the top N neighbors where the neighbors are sorted by out degree

def getCentralGraph(self, db, vertex, topN, depth):

print graphAnalytics.getCentralGraph(db, "'Amtrak'", 2, 1)

depth = 1
vertex = 'Amtrak'
["'Canada'", "'South_Dakota'"]
depth = 0
vertex = 'Canada'
["'National_Hockey_League'", "'North_America'"]
depth = 0
vertex = 'South_Dakota'
["'Iraq_War'", "'Nevada'"]
[["'Amtrak'", "'Canada'"], ["'Canada'", "'National_Hockey_League'"], ["'Canada'", "'North_America'"], ["'Amtrak'", "'South_Dakota'"], ["'South_Dakota'", "'Iraq_War'"], ["'South_Dakota'", "'Nevada'"]]
