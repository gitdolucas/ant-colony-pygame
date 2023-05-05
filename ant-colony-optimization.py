import pygame
from random import randint
import numpy as np
from math import pi, exp, cos, sin, floor

# COLORS
BLACK = (0, 0, 0) # background
GREY = (50, 50, 50) # sensors
WHITE = (255, 255, 255) # ant
YELLOW = (255, 191, 0) # nest
GREEN = (0, 255, 0) # food
RED = (255, 0, 0) # trail - to nest
BLUE = (0, 0, 255) # trail - to food

# CLOCK
CLOCK_SPEED = 100

# GRID
X_DIMENSION = 280
Y_DIMENSION = 120
RECT_SIZE = 3

# SCREEN SIZE
WIDTH = X_DIMENSION * RECT_SIZE
HEIGHT = Y_DIMENSION * RECT_SIZE

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)


# UTIL FOR DRAWING A STARTING POSITION FOR COLONY AT POSITION
NEST_SIZE = 10 # NOT USED YET
NEST_POSITION = (WIDTH / 2, HEIGHT / 2) # NEST AT CENTER POSITION
ANT_NUMBER = 5 # NUMBER OF ANTS IN SIMULATION
FOOD_CLUSTERS = 10 # NUMBER OF FOOD IN SIMULATION
RETRIEVED_FOOD = 0
EVAPORATION_RATE = 0.003
# GENERAL METHODS

# UTIL TO CREATE A MATRIX WITH DIMENSION SIZE
def GenerateMatrix():
    return [[0 for j in range(Y_DIMENSION)] for i in range(X_DIMENSION)]

# UTIL TO DRAW A RECT AT AN ESPECIFIC POSITION WITH AN ESPECIFIC COLOR
def DrawRect(position, color):
    # position must be in screen domain size (and not matrix domain)
    # ie. x * RECT_SIZE
    pygame.draw.rect(SCREEN, color, pygame.Rect(position[0], position[1], RECT_SIZE, RECT_SIZE))

# MATRICES
NEST_MATRIX = GenerateMatrix() # HOLDS TRAIL TO GUIDE ANTS TO THE NEST
ANT_POSITION_MATRIX = GenerateMatrix() # HOLDS ANT POSITIONS
FOOD_POSITION_MATRIX = GenerateMatrix() # HOLDS FOOD SOURCE POSITIONS
TO_NEST_MATRIX = GenerateMatrix() # HOLDS TRAIL TO GUIDE ANTS TO THE NEST
TO_FOOD_MATRIX = GenerateMatrix() # HOLDS TRAIL TO GUIDE ANTS TO THE FOOD SOURCE

class Ant():
    # -45 = right bottom
    # 0 = right
    # 45 = right bottom
    angle = 0
    position = (0, 0)
    isCarryingFood = False
    senseDistance = 5
    sensorAngle = 10
    senseDiameter = 2

    def sense(self, deg, matrix):
        deg = deg * pi / 180
        senseX = min(self.position[0] + self.senseDistance * cos(self.angle + deg), X_DIMENSION - 1)
        senseY = min(self.position[1] + self.senseDistance * sin(self.angle + deg), Y_DIMENSION - 1)

        # VISUALIZE SENSORS
        # DrawRect((senseX * RECT_SIZE, senseY * RECT_SIZE), GREY)

        return matrix[floor(senseX)][floor(senseY)] * deg     

    def senseLeft(self, matrix):
        return self.sense(self.sensorAngle * -1, matrix)

    def senseForward(self, matrix):
        return self.sense(self.sensorAngle * 0, matrix)

    def senseRight(self, matrix):
        return self.sense(self.sensorAngle, matrix)


    def __str__(self):
        return "angle: {}, position: {}, isCarryingFood: {}".format(self.angle, self.position, self.isCarryingFood) 

ANT_PROPS_LIST = []

# SIMULATION METHODS

# UTIL TO SET INITIAL RANDOM POSITION FOR FOOD SOURCES
def SetFoodInitialPosition():
    for food in range(FOOD_CLUSTERS):
        x = randint(0, X_DIMENSION - 1) 
        y = randint(0, Y_DIMENSION - 1)
        for i in range(10):
            for j in range(10):
                FOOD_POSITION_MATRIX[x - i][y - j] = 1 # NUMBER OF FOOD AVAILABLE IN THIS POSITION

# UTIL TO SET INITIAL ANT POSITION, ANGLE AND IF IS CARRYING FOOD
def SetAntInitialPosition():
    for antIndex in range(ANT_NUMBER):
        x = int(X_DIMENSION / 2)
        y = int(Y_DIMENSION / 2)
        ANT_POSITION_MATRIX[x][y] += 1
        ant = Ant()
        ant.angle = randint(0, 360)
        ant.position = (x, y)
        ANT_PROPS_LIST.append(ant)

# main function to update scene
def UpdateAnt(index):
    ant = ANT_PROPS_LIST[index]
    # print(ant)

    x = floor(ant.position[0]) # used only as index for matrices, need to be int
    y = floor(ant.position[1]) # used only as index for matrices, need to be int
    newX = ant.position[0] + cos(ant.angle)
    newY = ant.position[1] + sin(ant.angle)

    if (newX > X_DIMENSION or newX <= 0 or
        newY > Y_DIMENSION or newY <= 0):
        # getting outside the grid
        ant.angle = randint(0, 360)
    else:
        # check if it hits food
        if FOOD_POSITION_MATRIX[x][y] > 0:
            FOOD_POSITION_MATRIX[x][y] -= 1
            TO_FOOD_MATRIX[x][y] = 1
            ant.isCarryingFood = True
            ant.angle += 180 * pi / 180 # turn around to where it came from
        
        elif (X_DIMENSION, Y_DIMENSION) == (x, y):
            # check if hits nest
            # FOOD_POSITION_MATRIX[x][y] -= 1
            RETRIEVED_FOOD += 1
            print('Food count: %d' % RETRIEVED_FOOD)
            TO_NEST_MATRIX[x][y] = 1
            ant.isCarryingFood = False
            ant.angle += 180 * pi / 180 # turn around to where it came from
        
        if ant.isCarryingFood:
            # leave a trail to the food
            TO_FOOD_MATRIX[x][y] = 1
            # look for to_nest trail
            leftSensor = ant.senseLeft(TO_NEST_MATRIX)
            frontSensor = ant.senseForward(TO_NEST_MATRIX)
            rightSensor = ant.senseRight(TO_NEST_MATRIX)
            ant.angle += (leftSensor + frontSensor + rightSensor) * 0.3

        else:
            # leave a trail to the nest
            TO_NEST_MATRIX[x][y] = 1

            #look for food trail
            leftSensor = ant.senseLeft(TO_FOOD_MATRIX)
            frontSensor = ant.senseForward(TO_FOOD_MATRIX)
            rightSensor = ant.senseRight(TO_FOOD_MATRIX)
            ant.angle += (leftSensor + frontSensor + rightSensor) * 0.3

        # ant should wander in around
        ant.angle += (randint(0, 1) - 0.5) * 180 * 0.001  
        ant.position = (newX, newY)  

    
        ANT_POSITION_MATRIX[x][y] = 0
        ANT_POSITION_MATRIX[floor(newX)][floor(newY)] = 1
    # print(ant)

def LerpColor(color, intensity):
    # 0 - BLACK
    # 0/1 - linear interpolation
    # 1 - color
    r = BLACK[0] + intensity * (color[0] - BLACK[0])
    g = BLACK[1] + intensity * (color[1] - BLACK[1])
    b = BLACK[2] + intensity * (color[2] - BLACK[2])
    return (r, g, b)

def StartSimulation():
    SetAntInitialPosition()
    SetFoodInitialPosition()


StartSimulation()


pygame.init()
CLOCK = pygame.time.Clock()
IS_SIMULATION_RUNNING = True # APPLICATION CONTROL VARIABLE
while IS_SIMULATION_RUNNING:

    SCREEN.fill(BLACK)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            IS_SIMULATION_RUNNING = False

    if not IS_SIMULATION_RUNNING:
        break

    # DRAW CURRENT MATRIX STATUSES 
    for i in range(0, X_DIMENSION):
        for j in range(0, Y_DIMENSION):
            # order visually matters
            DrawRect((i * RECT_SIZE, j * RECT_SIZE), LerpColor(RED, TO_NEST_MATRIX[i][j])) if TO_NEST_MATRIX[i][j] > 0 else None # nest trail
            DrawRect((i * RECT_SIZE, j * RECT_SIZE), LerpColor(BLUE, TO_FOOD_MATRIX[i][j])) if TO_FOOD_MATRIX[i][j] > 0 else None # food trail
            DrawRect((i * RECT_SIZE, j * RECT_SIZE), GREEN) if FOOD_POSITION_MATRIX[i][j] > 0 else None # food
            DrawRect((i * RECT_SIZE, j * RECT_SIZE), WHITE) if ANT_POSITION_MATRIX[i][j] > 0 else None # ant

            # trail evaporation
            TO_NEST_MATRIX[i][j] -= EVAPORATION_RATE
            TO_FOOD_MATRIX[i][j] -= EVAPORATION_RATE

    
    # EVOLVE ANTS POSITION
    for i in range(ANT_NUMBER):
        UpdateAnt(i)


    # DRAW NEST POSITION
    DrawRect((X_DIMENSION, Y_DIMENSION), YELLOW)

    CLOCK.tick(CLOCK_SPEED)
    pygame.display.update()

pygame.quit()