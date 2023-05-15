from math import floor
from random import randint
from Utils import FOOD_CLUSTERS, FOOD_CLUSTERS_SIZE, GenerateMatrix, X_DIMENSION, Y_DIMENSION
from Nest import Nest


class Simulation():
    # pygame performance helper
    # __dirty_rects = []

    # simulation agents will be managed by each nest
    __nests = []

    # matrices
    __m_to_food_trail = None  # trail that lead agents to food
    __m_to_nest_trail = None  # trail that lead agets to nest
    __m_nest = None  # nest position so we can check when agent arrives
    __m_food = None  # food position so we can check when agent arrives
    __m_agent = None  # visual position of agents

    # CONSTRUCTOR -------------------------------------------------------------
    def __init__(self, n_nest_number, n_agents_per_nest):
        self.generateMatrices(X_DIMENSION, Y_DIMENSION)

        self.buildNests(
            X_DIMENSION, Y_DIMENSION, n_nest_number, n_agents_per_nest)
        self.disposeFood()

    # TODO: GET/SET DIRTY RECTS -----------------------------------------------------

    # def getDirtyRects(self):
    #     return self.__dirty_rects

    # def setDirtyRects(self, valueThatWillOverride):
    #     self.__dirty_rects = valueThatWillOverride
    #     return self.__dirty_rects

    # GET/SET NEST ------------------------------------------------------------

    def getNests(self):
        return self.__nests

    def setNests(self, valueThatWillOverride):
        self.__nests = valueThatWillOverride
        return self.__nests

    def addNest(self, newNest):
        self.__nests.append(newNest)
        return self.__nests

    # MATRICES GET/SET/UPDATE ----------------------------------------------------------

    def getMToFoodTrail(self):
        return self.__m_to_food_trail

    def setMToFoodTrail(self, value):
        self.__m_to_food_trail = value
        return self.__m_to_food_trail

    def updateMToFoodTrail(self, position, value):
        self.__m_to_food_trail[position[0]][position[1]] = value
        return self.__m_to_food_trail

    # ---

    def getMToNestTrail(self):
        return self.__m_to_nest_trail

    def setMToNestTrail(self, value):
        self.__m_to_nest_trail = value
        return self.__m_to_nest_trail

    def updateMToNestTrail(self, position, value):
        self.__m_to_nest_trail[position[0]][position[1]] = value
        return self.__m_to_nest_trail

    # ---

    def getMNests(self):
        return self.__m_nest

    def setMNests(self, value):
        self.__m_nest = value
        return self.__m_nest

    def updateMNests(self, position, value):
        self.__m_nest[position[0]][position[1]] = value
        return self.__m_nest

    # ---

    def getMFoods(self):
        return self.__m_food

    def setMFoods(self, value):
        self.__m_food = value
        return self.__m_food

    def updateMFoods(self, position, value):
        self.__m_food[position[0]][position[1]] = value
        return self.__m_food

    # ---

    def getMAgents(self):
        return self.__m_agent

    def setMAgents(self, value):
        self.__m_agent = value
        return self.__m_agent

    def updateMAgents(self, position, value):
        self.__m_agent[position[0]][position[1]] = value
        return self.__m_agent

    # METHODS ----------------------------------------------------------------

    def generateMatrices(self, X_DIMENSION, Y_DIMENSION):
        # initiate all matrices
        self.setMToFoodTrail(GenerateMatrix(X_DIMENSION, Y_DIMENSION))
        self.setMToNestTrail(GenerateMatrix(X_DIMENSION, Y_DIMENSION))
        self.setMNests(GenerateMatrix(X_DIMENSION, Y_DIMENSION))
        self.setMFoods(GenerateMatrix(X_DIMENSION, Y_DIMENSION))
        self.setMAgents(GenerateMatrix(X_DIMENSION, Y_DIMENSION))

    def buildNests(self, X_DIMENSION, Y_DIMENSION, n_nest_number, n_agents_per_nest):

        # creates each nest instance accordingly with number of nests in simulation
        for n in range(n_nest_number):
            initial_nest_position = (
                randint(0, X_DIMENSION), randint(0, Y_DIMENSION)
            )
            nest = Nest(n, initial_nest_position, n_agents_per_nest,
                        (randint(0, 255), randint(0, 255), randint(0, 255)), 2)

            self.addNest(nest)

            # draw nest position on nest matrix 
            for i in range(nest.getSize()):
                for j in range(nest.getSize()):
                    self.updateMNests(
                        (floor(initial_nest_position[0] - i / 2),
                         floor(initial_nest_position[1] - j / 2)),
                        1)

    def disposeFood(self):
        for food in range(FOOD_CLUSTERS):
            x = randint(0, X_DIMENSION - FOOD_CLUSTERS_SIZE) 
            y = randint(0, Y_DIMENSION - FOOD_CLUSTERS_SIZE)
            for i in range(FOOD_CLUSTERS_SIZE):
                for j in range(FOOD_CLUSTERS_SIZE):
                    self.updateMFoods((x - i, y - j), 1)

    def updateNests(self):
        for nest in self.getNests():
            nest.updateAgents(self)