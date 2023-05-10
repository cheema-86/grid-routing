#fuck it we ball
import pygame
import random
import math
import dicts
import heapq

#initializations
pygame.init()
window = pygame.display.set_mode((900,900))
clock = pygame.time.Clock()
running = True

#intial definitions
coordsList = [20,140,260,380,500,620,740,860]
nodesDict = dicts.nodeDictMaker()
keyList = list(nodesDict.keys())
valueList = list(nodesDict.values())
graph = dicts.graphMaker()

#this the weird squares that move
class Vehicle:
    def __init__ (self, posX, posY, destination):
        self.x = posX
        self.y = posY
        self.color = "red"
        #weird algorithm I came up with to decide start direction
        self.destination = destination
        #distance = [destination[0]-posX, destination[1]-posY]
        #minDis = min(distance)
        #distance[0] -= minDis
        #distance[1] -= minDis
        #self.direction = [1 if num > 0 else -1 if num < 0 else 0 for num in distance]
        #should have just stuck to sending everyone up
        self.direction = [0,0]
        self.size = 20
        self.deathCounter = 120
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.rect.update(self.x, self.y, self.size, self.size)

    def updateRoute(self, newDirection):
        self.direction = newDirection

    def display(self):
        pygame.draw.rect(window, self.color, self.rect)

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

def pathFinder(currVehicle):
    currNode = keyList[valueList.index([currVehicle.x,currVehicle.y])]
    route = dijkstra(graph,currNode,currVehicle.destination)
    nextNode = route[1]

    currCoords = valueList[keyList.index(currNode)]
    nextCoords = valueList[keyList.index(nextNode)]

    distance = [currCoords[0]-nextCoords[0],currCoords[1]-nextCoords[1]]

    direction = [-1 if num > 0 else 1 if num < 0 else 0 for num in distance]
    return direction


def drawGrid():
    for i in coordsList:
        #+10 is added to center the grid, can't be bothered to render the rectangle at the center so moved the grid ui
        pygame.draw.line(window, "black", (i+10,coordsList[0]+10), (i+10,coordsList[-1]+10))
        pygame.draw.line(window, "black", (coordsList[0]+10,i+10), (coordsList[-1]+10,i+10))

vehicleList = []
reachedList = []
def createVehicle():
    start = random.randint(0,63)
    x = nodesDict[start][0]
    y = nodesDict[start][1]

    dest = random.randint(0,63)
    while start == dest:
        dest = random.randint(0,63)
    vehicleList.append(Vehicle(x,y,dest))

for i in range(10):
    createVehicle()

#main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill("white")
    drawGrid()

    for vehicle in vehicleList:
        vehicle.display()

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
                vehicleList[i].color = "blue"
                print("Collision between vehicle", i, "and vehicle", j)

    for vehicle in vehicleList:
        #if vehicle at destination
        if [vehicle.x,vehicle.y] == nodesDict[vehicle.destination]:
            vehicle.color = "green"
            vehicle.direction = [0,0] #stop movement
            reachedList.append(vehicle)
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
    clock.tick(60)

pygame.quit()