import pygame
import random

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Grid dimensions
GRID_WIDTH = 50
GRID_HEIGHT = 50
CELL_SIZE = 10

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Vehicle Simulation")

class Vehicle:
    def __init__(self, x, y, color, direction = "up"):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction

    def move(self):
        if self.direction == "up":
            self.y -= 1
        elif self.direction == "down":
            self.y += 1
        elif self.direction == "left":
            self.x -= 1
        elif self.direction == "right":
            self.x += 1

    def draw(self):
        #print("Drawing vehicle at", self.x, self.y)
        # Draw vehicle on grid
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(window, self.color, rect)

grid = []
for y in range(GRID_HEIGHT):
    row = []
    for x in range(GRID_WIDTH):
        row.append(None)
    grid.append(row)

def createVehicle():
    if (random.randint(0,1)):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.choice([0, GRID_HEIGHT - 1])

        color = RED
        direction = random.choice(["up", "down"])
    else:
        x = random.choice([0, GRID_WIDTH - 1])
        y = random.randint(0, GRID_HEIGHT - 1)

        color = GREEN
        direction = random.choice(["right","left"])
    #color = random.choice([RED, GREEN, BLUE])
    vehicle = Vehicle(x, y, color, direction)
    vehicles.append(vehicle)
    grid[y][x] = vehicle


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
        grid[vehicle.y][vehicle.x] = None
        vehicle.move()
        if vehicle.x < 0 or vehicle.x >= GRID_WIDTH or vehicle.y < 0 or vehicle.y >= GRID_HEIGHT:

            vehicles.remove(vehicle)
            createVehicle()
        else:
            grid[vehicle.y][vehicle.x] = vehicle

    window.fill(BLACK)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] is not None:
                grid[y][x].draw()

    pygame.display.update()
