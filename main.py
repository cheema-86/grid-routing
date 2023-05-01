#fuck it we ball
import pygame
import random

#initializations
pygame.init()
window = pygame.display.set_mode((900,900))
clock = pygame.time.Clock()
running = True

#this the weird squares that move
class Vehicle:
    def __init__ (self, posX, posY, destination):
        self.x = posX
        self.y = posY
        self.color = "red"
        #weird algorithm I came up with to decide start direction
        self.destination = destination
        distance = [destination[0]-posX, destination[1]-posY]
        minDis = min(distance)
        distance[0] -= minDis
        distance[1] -= minDis
        self.direction = [1 if num > 0 else -1 if num < 0 else 0 for num in distance]
        #should have just stuck to sending everyone up
        self.size = 20
        self.deathCounter = 90
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.rect.update(self.x, self.y, self.size, self.size)

    def display(self):
        pygame.draw.rect(window, self.color, self.rect)

coordsList = [20,140,260,380,500,620,740,860]
def drawGrid():
    for i in coordsList:
        #+10 is added to center the grid, can't be bothered to render the rectangle at the center so moved the grid ui
        pygame.draw.line(window, "black", (i+10,coordsList[0]+10), (i+10,coordsList[-1]+10))
        pygame.draw.line(window, "black", (coordsList[0]+10,i+10), (coordsList[-1]+10,i+10))

vehicleList = []
reachedList = []
def createVehicle():
    x = random.choice(coordsList)
    y = random.choice(coordsList)
    dest = ((random.choice(coordsList),random.choice(coordsList)))
    while (x,y) == dest:
        dest = ((random.choice(coordsList),random.choice(coordsList)))
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
        vehicle.move()

        #if vehicle at destination
        if (vehicle.x,vehicle.y) == vehicle.destination:
            vehicle.color = "green"
            vehicle.direction = [0,0] #stop movement
            reachedList.append(vehicle)
            vehicleList.remove(vehicle)

        #if vehicle on intersection
        if vehicle.x in coordsList and vehicle.y in coordsList:
            if vehicle.x == vehicle.destination[0]:
                vehicle.direction = [0,1 if vehicle.destination[1]-vehicle.y > 0 else -1]
            if vehicle.y == vehicle.destination[1]:
                vehicle.direction = [1 if vehicle.destination[0]-vehicle.x > 0 else -1,0]
            ''''
            if vehicle.direction[0]:
                vehicle.direction = [0,random.choice([-1,1])]
            else:
                vehicle.direction = [random.choice([-1,1]),0]
            '''

        #if vehicle out of grid
        if vehicle.x < coordsList[0] or vehicle.x > coordsList[-1] or vehicle.y < coordsList[0] or vehicle.y > coordsList[-1]:
            vehicleList.remove(vehicle)
            createVehicle()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()