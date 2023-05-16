import pygame
import random
import dicts
import heapq
import copy

#initializations
pygame.init()
window = pygame.display.set_mode((900,900))
clock = pygame.time.Clock()
running = True

#intial definitions
coordsList = [20,140,260,380,500,620,740,860] #physical list of coords
nodesDict = dicts.nodeDictMaker() #external function to make a dictionary from the coordinate list
keyList = list(nodesDict.keys()) #list of all the nodes
valueList = list(nodesDict.values()) #list of all physical coordinates of the nodes
graph = dicts.graphMaker() #external function for initial creation of weighted graph

#definition of vehicle class
class Vehicle:
    def __init__ (self, posX, posY, destination):
        self.x = posX
        self.y = posY
        self.color = "red"
        self.destination = destination
        self.direction = [0,0]
        self.size = 20
        self.deathCounter = 120
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self): #function to move the vehicle along the path
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.rect.update(self.x, self.y, self.size, self.size)

    def updateRoute(self, newDirection): #function to update the direction of movement
        self.direction = newDirection

    def display(self): #function to display vehicle on screen
        pygame.draw.rect(window, self.color, self.rect)

#Dijkstra's algorithm
def dijkstra(graph, start, end=None):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    previous = {node: None for node in graph}
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node]:
            continue
        if curr_node == end:
            path = []
            while curr_node is not None:
                path.append(curr_node)
                curr_node = previous[curr_node]
            path.reverse()
            return path
        for neighbor, weight in graph[curr_node].items():
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = curr_node
                heapq.heappush(pq, (distance, neighbor))
    if end:
        return None
    path = []
    for node, prev in previous.items():
        if node is None:
            continue
        path.append(node)
        while prev is not None:
            path.append(prev)
            prev = previous[prev]
        path.reverse()
        break
    return path

#function to use the algorithm to provide vehicles with next node / direction
def pathFinder(currVehicle):
    currNode = keyList[valueList.index([currVehicle.x,currVehicle.y])]
    route = dijkstra(currentGraph(graph,currVehicle,vehicleList),currNode,currVehicle.destination)

    nextNode = route[1]

    currCoords = valueList[keyList.index(currNode)]
    nextCoords = valueList[keyList.index(nextNode)]

    distance = [currCoords[0]-nextCoords[0],currCoords[1]-nextCoords[1]]

    direction = [-1 if num > 0 else 1 if num < 0 else 0 for num in distance]
    return direction

#function to get a list of occupied nodes
def occupiedNodes(vList, cordLis):
    occupiedNode = []
    for v in vList:
        occupiedNode.append(keyList[valueList.index(nearestNode(v,cordLis))])
    return occupiedNode

#function to get a list of nodes which will be occupied next
def nextNodes(vList, cordLis):
    tempList = copy.copy(vList)
    nextNode = []
    for v in tempList:
        v.x += v.direction[0]*120
        v.y += v.direction[1]*120
        nextNode.append(keyList[valueList.index(nearestNode(v,cordLis))])
        v.x -= v.direction[0]*120
        v.y -= v.direction[1]*120
    return nextNode

#function to check which node is closest to a given vehicle
def nearestNode(veh,cordLis):
    return [min(cordLis, key=lambda x: abs(x - veh.x)),min(cordLis, key=lambda x: abs(x - veh.y))]

#function to update graph based on current position of vehicles
def currentGraph(djGraph, currVehicle, vehicleList):
    vList = vehicleList
    vList.remove(currVehicle)
    dGraph = copy.deepcopy(djGraph)

    occupiedNode = occupiedNodes(vList,coordsList)
    nextNode = nextNodes(vList,coordsList)
    occupiedNode.extend(nextNode)

    for node in dGraph:
        if node in occupiedNode:
            tempDict = dict(dGraph[node])
            for i in tempDict:
                #the path cost is temporarily changed from 1 to 20 to deter Dijkstra's algorithm from using this path
                tempDict[i] = 20 
            dGraph[node] = tempDict

    vList.append(currVehicle) 

    return dGraph

#drawing the background
def drawGrid():
    for i in coordsList:
        #+10 is added to center the grid with the rectangles
        pygame.draw.line(window, "black", (i+10,coordsList[0]+10), (i+10,coordsList[-1]+10))
        pygame.draw.line(window, "black", (coordsList[0]+10,i+10), (coordsList[-1]+10,i+10))

vehicleList = []
reachedList = []
reachedCount = 0
collisionCount = 0
#create vehicle function uses random start and end points for proof of concept
#this can be edited to provide user defined start and end points
def createVehicle():
    occupied = occupiedNodes(vehicleList,coordsList)
    start = random.randint(0,63)
    while start in occupied:
        start = random.randint(0,63)

    x = nodesDict[start][0]
    y = nodesDict[start][1]

    dest = random.randint(0,63)
    while start == dest:
        dest = random.randint(0,63)
    vehicleList.append(Vehicle(x,y,dest))

#creating 10 vehicles for the start of the simulation
for i in range(10):
    createVehicle()

#main loop
while running:
    #handling closing of application
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if reachedCount >= 100:
        running = False

    #darwing background
    window.fill("white")
    drawGrid()

    #displaying the vehicles which have reached
    for vehicle in reachedList:
        vehicle.deathCounter -= 1
        vehicle.display()
        if vehicle.deathCounter < 0:
            reachedList.remove(vehicle)
            createVehicle()

    #collision detection
    for i in range(len(vehicleList)):
        for j in range(i + 1, len(vehicleList)):
            if vehicleList[i].rect.colliderect(vehicleList[j].rect):
                #changing colours of vehicles in case they collide
                vehicleList[i].color = "blue"
                vehicleList[j].color = "blue"
                print("Collision between vehicle", i, "and vehicle", j)

    for vehicle in vehicleList:
        vehicle.display()

        #if vehicle at destination
        if [vehicle.x,vehicle.y] == nodesDict[vehicle.destination]:
            if vehicle.color == "blue":
                collisionCount += 1
            vehicle.color = "green"
            vehicle.direction = [0,0] #stop movement
            reachedList.append(vehicle)
            reachedCount += 1
            vehicleList.remove(vehicle)
        else:

            #if vehicle on intersection
            if [vehicle.x,vehicle.y] in valueList:
                vehicle.updateRoute(pathFinder(vehicle))


            #if vehicle out of grid
            if vehicle.x < coordsList[0] or vehicle.x > coordsList[-1] or vehicle.y < coordsList[0] or vehicle.y > coordsList[-1]:
                vehicleList.remove(vehicle)
                createVehicle()

            vehicle.move()

    pygame.display.flip()
    #clock.tick(60) #fps limiter

print("Reached:",reachedCount)
print("Collisions:",collisionCount)
pygame.quit()