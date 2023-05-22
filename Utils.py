from math import floor, pi, sqrt
import math
from random import randint, uniform
import pygame

# COLORS
BLACK = (0, 0, 0)  # background
GREY = (30, 30, 30)  # sensors
WHITE = (255, 255, 255)  # ant
YELLOW = (255, 191, 0)  # nest
GREEN = (0, 255, 0)  # food
RED = (255, 0, 0)  # trail - to nest
BLUE = (0, 0, 255)  # trail - to food

# CLOCK
CLOCK_SPEED = 100

# GRID
X_DIMENSION = 100
Y_DIMENSION = 100
RECT_SIZE = 6

# SCREEN SIZE
WIDTH = X_DIMENSION * RECT_SIZE
HEIGHT = Y_DIMENSION * RECT_SIZE

# UTIL FOR DRAWING A STARTING POSITION FOR COLONY AT POSITION
NEST_NUMBER = 1  # NUMBER OF AGENTS IN EACH NEST
NEST_SIZE = 4
# NEST_POSITION = (X_DIMENSION / 2, Y_DIMENSION / 2)
AGENTS_PER_NEST = 2  # NUMBER OF AGENTS IN EACH NEST
FOOD_CLUSTERS = 4  # NUMBER OF FOOD IN SIMULATION
FOOD_CLUSTERS_SIZE = 12  # NUMBER OF FOOD IN SIMULATION
EVAPORATION_RATE = 0.003
AGENT_ENERGY_COST = 0.99 # 1%
# DIRTY_RECTS = []
# NESTS = []
# AGENTS = []

# GENERAL METHODS

# UTIL TO CREATE A MATRIX WITH DIMENSION SIZE
def GenerateMatrix(x_dimension, y_dimension):
    return [[0 for j in range(y_dimension)] for i in range(x_dimension)]

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)

# UTIL TO DRAW A RECT AT AN ESPECIFIC POSITION WITH AN ESPECIFIC COLOR
def DrawRect(position, color):
    # position must be in screen domain size (and not matrix domain)
    # ie. x * RECT_SIZE
    pygame.draw.rect(
        SCREEN,
        color,
        pygame.Rect(position[0], position[1], RECT_SIZE, RECT_SIZE),
        floor(RECT_SIZE / 4),
        floor(RECT_SIZE / 2)
    )


def normalize(x, min_val, max_val):
    return 2 * (x - min_val) / (max_val - min_val) - 1

# helper for getting agent's next step
def getXYMagnitude(x, y):
    return sqrt(x**2 + y**2)


def degToRad(deg):
    return deg * pi / 180


def calculateAngle(A, B):
    # Calculate the dot product of A and B
    dotProduct = A[0] * B[0] + A[1] * B[1]

    # Calculate the magnitude of vector A
    magnitudeA = getXYMagnitude(A[0], A[1])

    # Calculate the magnitude of vector B
    magnitudeB = getXYMagnitude(B[0], B[1])

    # Calculate the cosine of the angle
    cosAngle = dotProduct / (magnitudeA * magnitudeB)

    # Calculate the angle in degrees using arccosine
    angle = degToRad(math.acos(max(-1, min(cosAngle, 1))))

    return angle


def LerpColor(color, intensity):
    # 0 - BLACK
    # 0/1 - linear interpolation
    # 1 - color
    r = BLACK[0] + min(intensity, 1) * (color[0] - BLACK[0])
    g = BLACK[1] + min(intensity, 1) * (color[1] - BLACK[1])
    b = BLACK[2] + min(intensity, 1) * (color[2] - BLACK[2])
    return (r, g, b)
