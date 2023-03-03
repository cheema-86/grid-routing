import pygame
import random

#initial variables
GRID_WIDTH = 50
GRID_HEIGHT = 50
CELL_SIZE = 10

#screen size
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

#defining colours here to reduce mess later
BG_COLOR = (0, 0, 0)
VEHICLE_COLOR = (255, 0, 0)
VEHICLE_COLOR_2 = (0, 255, 0)

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Vehicle Simulation")


#this needs some work
class Vehicle:
    def __init__(self, x, y, color, direction = "up"):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction

    def move(self): #iske paas direction hai, tere pass nahi
        if self.direction == "up":
            self.y -= 1
        elif self.direction == "down":
            self.y += 1
        elif self.direction == "left":
            self.x -= 1
        elif self.direction == "right":
            self.x += 1

    def draw(self):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(window, self.color, rect)


#currently randomly generating vehicles to check if simulation works, will be using proper algorithm later
def createVehicle():
    if (random.randint(0,1)):
        x = random.randint(0, (GRID_WIDTH - 1)//2)*2 #dividing by half then multiplying by 2 to only get even numbers
        y = random.choice([0, GRID_HEIGHT - 1])

        color = VEHICLE_COLOR
        direction = random.choice(["up", "down"]) #jada dimag nahi lagaya, marji se kisi bhi direction me chale jayega
    else:
        x = random.choice([0, GRID_WIDTH - 1])
        y = random.randint(0, (GRID_HEIGHT - 1)//2)*2 #dividing by half then multiplying by 2 to only get even numbers

        color = VEHICLE_COLOR_2
        direction = random.choice(["right","left"]) #jada dimag nahi lagaya, marji se kisi bhi direction me chale jayega
    vehicle = Vehicle(x, y, color, direction)
    vehicles.append(vehicle)


vehicles = []
for i in range(20):
    createVehicle()
    

running = True
clock = pygame.time.Clock()

while running:

    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for vehicle in vehicles:
        vehicle.move()
        if vehicle.x < 0 or vehicle.x >= GRID_WIDTH or vehicle.y < 0 or vehicle.y >= GRID_HEIGHT:
            #removing vehiles if they go off screen, then creating new one to replace it
            vehicles.remove(vehicle)
            createVehicle()
            
    window.fill(BG_COLOR)

    for vehicle in vehicles:
        vehicle.draw()

    pygame.display.update()
