from math import cos, floor, sin
from random import uniform

import numpy as np
from Utils import GREY, RECT_SIZE, X_DIMENSION, Y_DIMENSION, YELLOW, DrawRect, calculateAngle, degToRad, getXYMagnitude, normalize


class Agent():
    __position = None
    __isCarryingFood = False
    __nestReference = None
    __dxy = None
    __energy = 1

    def __init__(self, position, isCarryingFood, nestReference, dxy):
        self.setPosition(position)
        self.setIsCarryingFood(isCarryingFood)
        self.setNestReference(nestReference)
        self.setDXY(dxy)

    # GET/SET DXY
    def getDXY(self):
        return self.__dxy

    def setDXY(self, newDXY):
        self.__dxy = newDXY
        return self.__dxy
    
    # GET/SET DXY
    def getEnergy(self):
        self.setEnergy(self.__energy * 0.985)
        return self.__energy

    def setEnergy(self, newEnergy):
        self.__energy = newEnergy
        return self.__energy

    # GET/SET POSITION
    def getPosition(self):
        return self.__position

    def setPosition(self, newPosition):
        self.__position = newPosition
        return self.__position

    # GET/SET IS CARRYING FOOD
    def getIsCarryingFood(self):
        return self.__isCarryingFood

    def setIsCarryingFood(self, isCarryingFood):
        self.__isCarryingFood = isCarryingFood
        return self.__isCarryingFood

    # GET/SET NEST
    def getNestReference(self):
        return self.__nestReference

    def setNestReference(self, nestReference):
        self.__nestReference = nestReference
        return self.__nestReference

    def getFood(self):
        self.setIsCarryingFood(True)
        self.setEnergy(1)
        self.turnAround()
    
    def releaseFood(self):
        self.setIsCarryingFood(False)
        self.setEnergy(1)
        self.turnAround()

    def sense(self, matrix):
        # This method will generate a box around the ant
        # After that, focus on dxy[0]*r[0] + dxy[1]*r[1] >= 0
        # and set DXY to the mean of present value in matrix

        # normalized direction
        [dx, dy] = self.getDXY()
        directionMagnitude = getXYMagnitude(
            dx, dy)

        if directionMagnitude != 0:
            [ndx, ndy] = [
                dx / directionMagnitude,
                dy / directionMagnitude,
            ]
        else:
            return

        # print(dx, dy)
        # absolute direction (direction debbugging)
        AD = (self.getPosition()[0] + ndx, self.getPosition()[1] + ndy)

        maxConcentration = 0.15

        # Area of sense
        for i in range(12):
            rx = 6 - i
            for j in range(12):
                ry = 6 - j
                # normalized point of interest
                piMagnitude = getXYMagnitude(
                    rx, ry)
                if piMagnitude != 0:
                    [nrx, nry] = [
                        rx / piMagnitude,
                        ry / piMagnitude,
                    ]
                if (ndx * nrx) + (ndy * nry) >= calculateAngle(self.getPosition(), AD):
                    # inside the agent's view

                    [x, y] = max(0, min(X_DIMENSION - 1, self.getPosition()[0] + rx)), max(
                        0, min(Y_DIMENSION - 1, self.getPosition()[1] + ry))
                    if matrix[floor(x)][floor(y)] > maxConcentration:  # Consider bigger than previous concentrations
                        maxConcentration = matrix[floor(x)][floor(y)]
                        self.setDXY((floor(rx), floor(ry)))

                    # PI = (
                    #     self.getPosition()[0] + rx,
                    #     self.getPosition()[1] + ry,
                    # )
                    # DrawRect(((PI[0]) * RECT_SIZE , (PI[1])* RECT_SIZE), GREY)

        # Absolute direction visualization
        # DrawRect(((AD[0]) * RECT_SIZE, (AD[1]) * RECT_SIZE), YELLOW)
        
        # return maxPosition
    

    def turnAround(self):
        self.setDXY((
            self.getDXY()[0] * -1,
            self.getDXY()[1] * -1,
        ))
        return self.getDXY()

    def move(self, x, y, newDx, newDy):
        if (x > X_DIMENSION or x <= 0 or
                y > Y_DIMENSION or y <= 0):
            # self.turnAround()
            self.setDXY((
                uniform(-1, 1),
                uniform(-1, 1),
            ))
        else:
            self.setPosition((
                x,
                y,
            ))
            self.setDXY((newDx, newDy))
        return self.getPosition()

    def wander(self):

        # get vector of direction
        [dx, dy] = self.getDXY()

        # variate over current direction
        variationX = uniform(-0.2, 0.2)
        variationY = uniform(-0.2, 0.2)
        [newDx, newDy] = (
            normalize(dx + variationX, -1, 1),
            normalize(dy + variationY, -1, 1),
        )
        # print(newDx, newDy)
        # xWander = uniform(dx * -variation, dx * variation)
        # yWander = uniform(dy * -variation , dy * variation)

        # get magnitude of direction + wander
        directionMagnitude = getXYMagnitude(
            newDx, newDy)

        # step to be added to current position
        nextPositionStep = (
            (newDx) / directionMagnitude,
            (newDy) / directionMagnitude
        )

        # next position
        x = self.getPosition()[0] + nextPositionStep[0]
        y = self.getPosition()[1] + nextPositionStep[1]

        # move agent
        return self.move(x, y, newDx, newDy)

    def __str__(self):
        return '''dxy: {}, position: {}, isCarryingFood: {}, nest reference: {}'''.format(self.getDXY(), self.getPosition(), self.getIsCarryingFood(), self.getNestReference())
