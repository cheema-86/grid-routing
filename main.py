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
    def __init__ (self, posX, posY):
        self.x = posX
        self.y = posY
        self.direction = [0,1]
        self.size = 20
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.rect.update(self.x, self.y, self.size, self.size)

    def display(self):
        #self.rect.update(self.x, self.y, self.size, self.size)
        pygame.draw.rect(window, "red", self.rect)

coordsList = [20,140,260,380,500,620,740,860]
def drawGrid():
    for i in coordsList:
        pygame.draw.line(window, "black", (i+10,coordsList[0]+10), (i+10,coordsList[-1]+10))
        pygame.draw.line(window, "black", (coordsList[0]+10,i+10), (coordsList[-1]+10,i+10))

vehicleList = []
def createVehicle():
    vehicleList.append(Vehicle(random.choice(coordsList),random.choice(coordsList)))

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

    #collision detection
    for i in range(len(vehicleList)):
        for j in range(i + 1, len(vehicleList)):
            if vehicleList[i].rect.colliderect(vehicleList[j].rect):
                print("Collision between vehicle", i, "and vehicle", j)

    for vehicle in vehicleList:
        vehicle.move()

        #if vehicle on intersection
        if vehicle.x in coordsList and vehicle.y in coordsList:
            if vehicle.direction[0]:
                vehicle.direction = [0,random.choice([-1,1])]
            else:
                vehicle.direction = [random.choice([-1,1]),0]

        #if vehicle out of grid
        if vehicle.x < coordsList[0] or vehicle.x > coordsList[-1] or vehicle.y < coordsList[0] or vehicle.y > coordsList[-1]:
            vehicleList.remove(vehicle)
            createVehicle()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()