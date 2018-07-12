import math, json, re
from urllib.request import urlopen


def download():
	graph = {}
	page = urlopen("file:///G:/Summer%20Research%20Project/cur4.json")
	jsrates = json.loads(page.read())
	pattern = re.compile("([A-Z]{3})_([A-Z]{3})")
	for key in jsrates:
		matches = pattern.match(key)
		conversion_rate = -math.log(float(jsrates[key]))
		from_rate = matches.group(1).encode('ascii','ignore')
		to_rate = matches.group(2).encode('ascii','ignore')
		if from_rate != to_rate:
			if from_rate not in graph:
				graph[from_rate] = {}
			graph[from_rate][to_rate] = float(conversion_rate)
	return graph

# Step 1: For each node,construct the destination and predecessor
def initialize(graph, source):
    d = {} #destination
    p = {} #predecessor
    for node in graph:
        d[node] = float('Inf') # Initially the rest of nodes are far away
        p[node] = None
    d[source] = 0 # For the source we know how to reach
    return d, p
 
def relax(node, neighbour, graph, d, p):
    # If the distance between the node and the neighbour is lower than the one we have at present
    if d[neighbour] > d[node] + graph[node][neighbour]:
        # Store this lesser distance
        d[neighbour]  = d[node] + graph[node][neighbour]
        p[neighbour] = node
 
def track_negative_cycle(p, start):
	arbitrageLoop = [start]
	next_node = start
	while True:
		next_node = p[next_node]
		if next_node not in arbitrageLoop:
			arbitrageLoop.append(next_node)
		else:
			arbitrageLoop.append(next_node)
			arbitrageLoop = arbitrageLoop[arbitrageLoop.index(next_node):]
			return arbitrageLoop


def bellman_ford(graph, source):
    d, p = initialize(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for j in graph:
            for k in graph[j]: #For each neighbour of j
                relax(j, k, graph, d, p) #Lets relax it


    # Step 3: check for negative-weight cycles
    for j in graph:
        for k in graph[j]:
        	if d[k] < d[j] + graph[j][k]:
        		return(track_negative_cycle(p, source))
    return None

paths = []

graph = download()

for key in graph:
	path = bellman_ford(graph, key)
	if path not in paths and not None:
		paths.append(path)

for path in paths:
	if path == None:
		print("No opportunity here. Try again!")
	else:
		money = 700
		print ("Starting with %(money)i in %(currency)s" % {"money":money,"currency":path[0]})

		for i,value in enumerate(path):
			if i+1 < len(path):
				start = path[i]
				end = path[i+1]
				rate = math.exp(graph[start][end])
				money *= rate
				print ("%(start)s to %(end)s at %(rate)f = %(money)f" % {"start":start,"end":end,"rate":rate,"money":money})
	print ("\n")
