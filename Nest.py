from math import floor
from random import uniform
from Agent import Agent

class Nest():
    __id = None
    __position = None
    __size = None
    __color = None
    __agents = []
    __retrievedFood = 0

    def __init__(self, id, nestPosition, n_agents_per_nest, color, size):
        
        self.setId(id)
        self.setPosition(nestPosition)
        self.setColor(color)
        self.setSize(size)

        # create agents that will be managed
        for i in range(n_agents_per_nest):
                self.addAgents(Agent(nestPosition, False, id,
                                  (uniform(-1, 1), uniform(-1, 1))))

    # GET/SET ID --------------------------------------------------------
    def getId(self):
        return self.__id

    def setId(self, newId):
        self.__id = newId
        return self.__id
    
    # GET/SET POSITION --------------------------------------------------
    def getPosition(self):
        return self.__position

    def setPosition(self, newPosition):
        self.__position = newPosition
        return self.__position
    
    # GET/SET SIZE ------------------------------------------------------
    def getSize(self):
        return self.__size

    def setSize(self, newSize):
        self.__size = newSize
        return self.__size
    
    # GET/SET COLOR -----------------------------------------------------
    def getColor(self):
        return self.__color

    def setColor(self, newColor):
        self.__color = newColor
        return self.__color
    
    # GET/SET AGENTS ----------------------------------------------------
    def getAgents(self):
        return self.__agents

    def setAgents(self, agents):
        self.__agents = agents
        return self.__agents
    
    def addAgents(self, agent):
        self.__agents.append(agent)
        return self.__agents
    
    def updateAgents(self, simulation):
        for agent in self.getAgents():



            # used only as index for matrices, need to be int
            x = floor(agent.getPosition()[0])
            # used only as index for matrices, need to be int
            y = floor(agent.getPosition()[1])

            simulation.updateMAgents((x, y), 0)

            # [x, y] = agent.wander()
            if agent.getIsCarryingFood():
                simulation.updateMToFoodTrail((floor(x), floor(y)), 1 * agent.getEnergy())
                agent.sense(simulation.getMToNestTrail())
                agent.sense(simulation.getMNests())
                if(simulation.getMNests()[floor(x)][floor(y)] > 0):
                    # simulation.updateMFoods((floor(x), floor(y)), 0)
                    agent.releaseFood()
                    simulation.foodSuccessfullyColected()
            else:
                simulation.updateMToNestTrail((floor(x), floor(y)), 1 * agent.getEnergy())
                agent.sense(simulation.getMToFoodTrail())
                agent.sense(simulation.getMFoods())
                # agent.sense(simulation.getMFoods())
                if(simulation.getMFoods()[floor(x)][floor(y)] > 0):
                    simulation.updateMFoods((floor(x), floor(y)), 0)
                    agent.getFood()


            # used only as index for matrices, need to be int
            x = floor(agent.getPosition()[0])
            # used only as index for matrices, need to be int
            y = floor(agent.getPosition()[1])
            simulation.updateMAgents((floor(x), floor(y)), 1)
                
    # class string ------------------------------------------------------

    def __str__(self):
        return "agents: {}, position: {}".format(len(self.getAgents()), self.getPosition()) 
