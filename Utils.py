from math import floor, pi, sqrt
import math
from random import randint, uniform
import pygame

# COLORS
BLACK = (0, 0, 0)  # background
GREY = (10, 10, 10)  # sensors
WHITE = (255, 255, 255)  # ant
YELLOW = (255, 191, 0)  # nest
GREEN = (0, 255, 0)  # food
RED = (255, 0, 0)  # trail - to nest
BLUE = (0, 0, 255)  # trail - to food

# CLOCK
CLOCK_SPEED = 10

# GRID
X_DIMENSION = 200
Y_DIMENSION = 200
RECT_SIZE = 3

# SCREEN SIZE
WIDTH = X_DIMENSION * RECT_SIZE
HEIGHT = Y_DIMENSION * RECT_SIZE

# UTIL FOR DRAWING A STARTING POSITION FOR COLONY AT POSITION
NEST_SIZE = 4
NEST_POSITION = (X_DIMENSION / 2, Y_DIMENSION / 2)
ANT_NUMBER = 2 # NUMBER OF ANTS IN SIMULATION
FOOD_CLUSTERS = 7  # NUMBER OF FOOD IN SIMULATION
FOOD_CLUSTERS_SIZE = 12 # NUMBER OF FOOD IN SIMULATION
EVAPORATION_RATE = 0.99
DIRTY_RECTS = []
NESTS = []
AGENTS = []

# GENERAL METHODS

# UTIL TO CREATE A MATRIX WITH DIMENSION SIZE


def GenerateMatrix(x_dimension, y_dimension):
    return [[0 for j in range(y_dimension)] for i in range(x_dimension)]

# helper for getting agent's next step 
def getXYMagnitude(x, y):
    return sqrt(x**2 + y**2)
    
# def normalize(value, min, max):
    # return (2 * (value - min) / (max - min)) - 1.0

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)

# UTIL TO DRAW A RECT AT AN ESPECIFIC POSITION WITH AN ESPECIFIC COLOR


def DrawRect(position, color):
    # position must be in screen domain size (and not matrix domain)
    # ie. x * RECT_SIZE
    pygame.draw.rect(SCREEN, color, pygame.Rect(
        position[0], position[1], RECT_SIZE, RECT_SIZE))

def normalize(x, min_val, max_val):
    return 2 * (x - min_val) / (max_val - min_val) - 1

def degToRad(deg):
    return deg * pi / 180

def calculateAngle(A, B):
    dotProduct = A[0] * B[0] + A[1] * B[1]  # Calculate the dot product of A and B
    magnitudeA = math.sqrt(A[0]**2 + A[1]**2)  # Calculate the magnitude of vector A
    magnitudeB = math.sqrt(B[0]**2 + B[1]**2)  # Calculate the magnitude of vector B
    cosAngle = dotProduct / (magnitudeA * magnitudeB)  # Calculate the cosine of the angle

    angle = degToRad(math.acos(max(-1, min(cosAngle, 1))))  # Calculate the angle in degrees using arccosine

    return angle

# UTIL TO SET INITIAL RANDOM POSITION FOR FOOD SOURCES


# def SetFoodInitialPosition():
#     for food in range(FOOD_CLUSTERS):
#         x = randint(0, X_DIMENSION - FOOD_CLUSTERS_SIZE)
#         y = randint(0, Y_DIMENSION - FOOD_CLUSTERS_SIZE)
#         for i in range(FOOD_CLUSTERS_SIZE):
#             for j in range(FOOD_CLUSTERS_SIZE):
#                 # NUMBER OF FOOD AVAILABLE IN THIS POSITION
#                 M_FOOD_POSITION_MATRIX[x - i][y - j] = 1

# UTIL TO SET INITIAL ANT POSITION, ANGLE AND IF IS CARRYING FOOD


# def SetInitialPosition():
#     for antIndex in range(ANT_NUMBER):
#         x = int(NEST_POSITION[0])
#         y = int(NEST_POSITION[1])
#         M_ANT_POSITION_MATRIX[x][y] += 1
#         ant = ()
#         ant.angle = randint(0, 360)
#         ant.position = (x, y)
#         NESTS.append(ant)
#         AGENTS.append(ant)

# main function to update scene


# def Update(index):
#     ant = NESTS[index]
#     ant = AGENTS[index]

#     # used only as index for matrices, need to be int
#     x = floor(ant.position[0])
#     # used only as index for matrices, need to be int
#     y = floor(ant.position[1])
#     newX = ant.position[0] + cos(ant.angle)
#     newY = ant.position[1] + sin(ant.angle)

#     if (newX > X_DIMENSION or newX <= 0 or
#             newY > Y_DIMENSION or newY <= 0):
#         # getting outside the grid
#         # ant.angle = randint(0, 360)
#         ant.setAngle(randint(180, 360))

#     else:
#         if ant.isCarryingFood:
#             # this ant is looking for the nest to retrieve the food
#             # leave a trail to the food
#             # ant.senseAndLock(M_NEST_MATRIX)
#             M_TO_FOOD_MATRIX[x][y] = 1

#             # ant.angle += ant.lookForTrail()
#             ant.setAngle(ant.angle + ant.lookForTrail())
#             if M_NEST_MATRIX[x][y] > 0:
#                 M_TO_NEST_MATRIX[x][y] += 1
#                 ant.isCarryingFood = False
#                 # ant.angle += 180 * pi / 180 # turn around to where it came from
#                 ant.locked = False
#                 ant.setAngle(ant.angle + degToRad(180))

#             # look for to_nest trail

#         else:
#             # this ant is looking for food
#             # leave a trail to the nest

#             # ant.senseAndLock(M_FOOD_POSITION_MATRIX)
#             M_TO_NEST_MATRIX[x][y] += 1

#             # look for food trail
#             # ant.angle += ant.lookForFoodTrail()
#             ant.setAngle(ant.angle + ant.lookForFoodTrail())

#             if M_FOOD_POSITION_MATRIX[x][y] > 0:
#                 M_FOOD_POSITION_MATRIX[x][y] -= 1
#                 M_TO_FOOD_MATRIX[x][y] = 1
#                 ant.isCarryingFood = True
#                 # ant.angle += 180 * pi / 180 # turn around to where it came from
#                 ant.locked = False
#                 ant.setAngle(ant.angle + degToRad(180))

#         ant.setAngle(ant.angle + (randint(0, 1) - 0.5) * 90 * 0.001)

#         # newX = ant.position[0] + cos(ant.angle)
#         # newY = ant.position[1] + sin(ant.angle)

#         # ant should wander in around
#         # ant.angle += (randint(0, 1) - 0.5) * 90 * 0.001
#         ant.position = (newX, newY)

#         M_ANT_POSITION_MATRIX[x][y] = 0
#         M_ANT_POSITION_MATRIX[floor(newX)][floor(newY)] = 1
    # print(ant)


def LerpColor(color, intensity):
    # 0 - BLACK
    # 0/1 - linear interpolation
    # 1 - color
    r = BLACK[0] + min(intensity, 1) * (color[0] - BLACK[0])
    g = BLACK[1] + min(intensity, 1) * (color[1] - BLACK[1])
    b = BLACK[2] + min(intensity, 1) * (color[2] - BLACK[2])
    return (r, g, b)


