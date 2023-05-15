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
CLOCK_SPEED = 50

# GRID
X_DIMENSION = 100
Y_DIMENSION = 100
RECT_SIZE = 5

# SCREEN SIZE
WIDTH = X_DIMENSION * RECT_SIZE
HEIGHT = Y_DIMENSION * RECT_SIZE

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)

# UTIL FOR DRAWING A STARTING POSITION FOR COLONY AT POSITION
NEST_SIZE = 10
NEST_POSITION = (X_DIMENSION / 2, Y_DIMENSION / 2) 
ANT_NUMBER = 50 # NUMBER OF ANTS IN SIMULATION
FOOD_CLUSTERS = 10 # NUMBER OF FOOD IN SIMULATION
FOOD_CLUSTERS_SIZE = 4 # NUMBER OF FOOD IN SIMULATION
EVAPORATION_RATE = 0.995
INDIVIDUAL_ANTS = []

# GENERAL METHODS

# UTIL TO CREATE A MATRIX WITH DIMENSION SIZE
def GenerateMatrix():
    return [[0 for j in range(Y_DIMENSION)] for i in range(X_DIMENSION)]

# UTIL TO DRAW A RECT AT AN ESPECIFIC POSITION WITH AN ESPECIFIC COLOR
def DrawRect(position, color):
    # position must be in screen domain size (and not matrix domain)
    # ie. x * RECT_SIZE
    pygame.draw.rect(SCREEN, color, pygame.Rect(position[0], position[1], RECT_SIZE, RECT_SIZE))

def degToRad(deg):
    return deg * pi / 180

# MATRICES
M_NEST_MATRIX = GenerateMatrix() # HOLDS NEST POSITION
M_ANT_POSITION_MATRIX = GenerateMatrix() # HOLDS ANT POSITIONS
M_FOOD_POSITION_MATRIX = GenerateMatrix() # HOLDS FOOD SOURCE POSITIONS
M_TO_NEST_MATRIX = GenerateMatrix() # HOLDS TRAIL TO GUIDE ANTS TO THE NEST
M_TO_FOOD_MATRIX = GenerateMatrix() # HOLDS TRAIL TO GUIDE ANTS TO THE FOOD SOURCE

class Ant():
    angle = 0 # angle in radians
    position = (0, 0)
    isCarryingFood = False
    senseDistance = 6
    sensorAngle = 10
    trailDesirability = 1
    fov = 4 # distance of view
    locked = False
    # senseDiameter = 2

    def setAngle(self, angle):
        if not self.locked:
            self.angle = angle

    def sense(self, deg, matrix):
        deg = degToRad(deg)
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

    def senseNearby(self, matrix):
        
        for step in range(self.fov):
            toTheLeft = self.angle - degToRad(step * self.sensorAngle)
            keepForward = self.angle
            toTheRight = self.angle + degToRad(step * self.sensorAngle)
            left = (
                min((self.position[0] + step * cos(toTheLeft)), X_DIMENSION - 1),  
                min((self.position[1] + step * sin(toTheLeft)), Y_DIMENSION - 1)
            )
            forward = (
                min((self.position[0] + step * cos(keepForward)), X_DIMENSION - 1),
                min((self.position[1] + step * sin(keepForward)), Y_DIMENSION - 1)
            )
            right = (
                min((self.position[0] + step * cos(toTheRight)), X_DIMENSION - 1),
                min((self.position[1] + step * sin(toTheRight)), Y_DIMENSION - 1)
            )
            
            # print(left)
            if(matrix[floor(left[0])][floor(left[1])] > 0):
                self.setAngle(toTheLeft)
                self.locked = True
                # print('left found food!')
            if(matrix[floor(forward[0])][floor(forward[1])] > 0):
                self.setAngle(keepForward)
                self.locked = True
                # print('forward found food!')
            if(matrix[floor(right[0])][floor(right[1])] > 0):
                self.setAngle(toTheRight)
                self.locked = True
                # print('right found food!')
            # DrawRect( (left[0]  * RECT_SIZE,left[1]  * RECT_SIZE), YELLOW)
            # DrawRect( (forward[0] * RECT_SIZE,forward[1] * RECT_SIZE) , BLUE)
            # DrawRect( (right[0] * RECT_SIZE,right[1] * RECT_SIZE) , RED)
            


    def lookForFoodTrail(self):
        self.senseNearby(M_FOOD_POSITION_MATRIX)
        leftSensor = self.senseLeft(M_TO_FOOD_MATRIX)
        frontSensor = self.senseForward(M_TO_FOOD_MATRIX)
        rightSensor = self.senseRight(M_TO_FOOD_MATRIX)
        return (leftSensor + frontSensor + rightSensor) 

    def lookForNestTrail(self):
        self.senseNearby(M_NEST_MATRIX)
        leftSensor = self.senseLeft(M_TO_NEST_MATRIX)
        frontSensor = self.senseForward(M_TO_NEST_MATRIX)
        rightSensor = self.senseRight(M_TO_NEST_MATRIX)
        return (leftSensor + frontSensor + rightSensor)

    def senseAndLock(self, matrix):
        return 0
        # leftSensor = self.senseLeft(matrix)
        # frontSensor = self.senseForward(matrix)
        # rightSensor = self.senseRight(matrix)
        # self.setAngle(leftSensor + frontSensor + rightSensor)
        # self.locked = leftSensor + frontSensor + rightSensor > 0

        
        
    def __str__(self):
        return "angle: {}, position: {}, isCarryingFood: {}".format(self.angle, self.position, self.isCarryingFood) 



# SIMULATION METHODS

# UTIL TO SET INITIAL RANDOM POSITION FOR FOOD SOURCES
def SetNestPosition():
    for i in range(NEST_SIZE):
        for j in range(NEST_SIZE):
            M_NEST_MATRIX[floor(NEST_POSITION[0] - i / 2 )][floor(NEST_POSITION[1] - j / 2 )] = 1

# UTIL TO SET INITIAL RANDOM POSITION FOR FOOD SOURCES
def SetFoodInitialPosition():
    for food in range(FOOD_CLUSTERS):
        x = randint(0, X_DIMENSION - FOOD_CLUSTERS_SIZE) 
        y = randint(0, Y_DIMENSION - FOOD_CLUSTERS_SIZE)
        for i in range(FOOD_CLUSTERS_SIZE):
            for j in range(FOOD_CLUSTERS_SIZE):
                M_FOOD_POSITION_MATRIX[x - i][y - j] = 1 # NUMBER OF FOOD AVAILABLE IN THIS POSITION

# UTIL TO SET INITIAL ANT POSITION, ANGLE AND IF IS CARRYING FOOD
def SetAntInitialPosition():
    for antIndex in range(ANT_NUMBER):
        x = int(NEST_POSITION[0])
        y = int(NEST_POSITION[1])
        M_ANT_POSITION_MATRIX[x][y] += 1
        ant = Ant()
        ant.angle = randint(0, 360)
        ant.position = (x, y)
        INDIVIDUAL_ANTS.append(ant)

# main function to update scene
def UpdateAnt(index):
    ant = INDIVIDUAL_ANTS[index]

    x = floor(ant.position[0]) # used only as index for matrices, need to be int
    y = floor(ant.position[1]) # used only as index for matrices, need to be int
    newX = ant.position[0] + cos(ant.angle)
    newY = ant.position[1] + sin(ant.angle)

    if (newX > X_DIMENSION or newX <= 0 or
        newY > Y_DIMENSION or newY <= 0):
        # getting outside the grid
        # ant.angle = randint(0, 360)
        ant.setAngle(randint(180, 360))

    else:
        if ant.isCarryingFood:
            # this ant is looking for the nest to retrieve the food
            # leave a trail to the food
            # ant.senseAndLock(M_NEST_MATRIX)
            M_TO_FOOD_MATRIX[x][y] = 1

            # ant.angle += ant.lookForNestTrail()
            ant.setAngle(ant.angle + ant.lookForNestTrail())
            if M_NEST_MATRIX[x][y] > 0:
                M_TO_NEST_MATRIX[x][y] += 1
                ant.isCarryingFood = False
                # ant.angle += 180 * pi / 180 # turn around to where it came from
                ant.locked = False
                ant.setAngle(ant.angle + degToRad(180))

            # look for to_nest trail

        else:
            # this ant is looking for food
            # leave a trail to the nest

            # ant.senseAndLock(M_FOOD_POSITION_MATRIX)
            M_TO_NEST_MATRIX[x][y] += 1

            #look for food trail
            # ant.angle += ant.lookForFoodTrail()
            ant.setAngle(ant.angle + ant.lookForFoodTrail())
        
            if M_FOOD_POSITION_MATRIX[x][y] > 0:
                M_FOOD_POSITION_MATRIX[x][y] -= 1
                M_TO_FOOD_MATRIX[x][y] = 1
                ant.isCarryingFood = True
                # ant.angle += 180 * pi / 180 # turn around to where it came from      
                ant.locked = False
                ant.setAngle(ant.angle + degToRad(180))

        ant.setAngle(ant.angle + (randint(0, 1) - 0.5) * 90 * 0.001)

        # newX = ant.position[0] + cos(ant.angle)
        # newY = ant.position[1] + sin(ant.angle)

        # ant should wander in around
        # ant.angle += (randint(0, 1) - 0.5) * 90 * 0.001  
        ant.position = (newX, newY)  

        M_ANT_POSITION_MATRIX[x][y] = 0
        M_ANT_POSITION_MATRIX[floor(newX)][floor(newY)] = 1
    # print(ant)

def LerpColor(color, intensity):
    # 0 - BLACK
    # 0/1 - linear interpolation
    # 1 - color
    r = BLACK[0] + min(intensity,1) * (color[0] - BLACK[0])
    g = BLACK[1] + min(intensity,1) * (color[1] - BLACK[1])
    b = BLACK[2] + min(intensity,1) * (color[2] - BLACK[2])
    return (r, g, b)

def StartSimulation():
    SetNestPosition()
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
        # if event.type == pygame.KEYDOWN:

    if not IS_SIMULATION_RUNNING:
        break

    # DRAW CURRENT MATRIX STATUSES 
    for i in range(0, X_DIMENSION):
        for j in range(0, Y_DIMENSION):
            # order visually matters
            DrawRect((i * RECT_SIZE, j * RECT_SIZE), LerpColor(RED, M_TO_NEST_MATRIX[i][j])) if M_TO_NEST_MATRIX[i][j] > 0 else None # nest trail
            DrawRect((i * RECT_SIZE, j * RECT_SIZE), LerpColor(BLUE, M_TO_FOOD_MATRIX[i][j])) if M_TO_FOOD_MATRIX[i][j] > 0 else None # food trail
            DrawRect((i * RECT_SIZE, j * RECT_SIZE), GREEN) if M_FOOD_POSITION_MATRIX[i][j] > 0 else None # food
            DrawRect((i * RECT_SIZE, j * RECT_SIZE), WHITE) if M_ANT_POSITION_MATRIX[i][j] > 0 else None # ant
            DrawRect((i * RECT_SIZE, j * RECT_SIZE), YELLOW) if M_NEST_MATRIX[i][j] > 0 else None # nest

            # trail evaporation
            M_TO_NEST_MATRIX[i][j] *= EVAPORATION_RATE
            M_TO_FOOD_MATRIX[i][j] *= EVAPORATION_RATE

    
    # EVOLVE ANTS POSITION
    for i in range(ANT_NUMBER):
        UpdateAnt(i)

    CLOCK.tick(CLOCK_SPEED)
    pygame.display.update()

pygame.quit()