from Utils import SCREEN, CLOCK_SPEED, WIDTH, HEIGHT, LerpColor, BLACK, GREEN, RED, BLUE, WHITE, YELLOW, X_DIMENSION, Y_DIMENSION, EVAPORATION_RATE, ANT_NUMBER, DrawRect, RECT_SIZE
from Simulation import Simulation
import pygame
from profilehooks import profile


# @profile
def main():

    simulation = Simulation(4, 20)

    pygame.init()
    CLOCK = pygame.time.Clock()
    IS_SIMULATION_RUNNING = True  # APPLICATION CONTROL VARIABLE
    while IS_SIMULATION_RUNNING:

        SCREEN.fill(BLACK)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                IS_SIMULATION_RUNNING = False
            # if event.type == pygame.KEYDOWN:

        if not IS_SIMULATION_RUNNING:
            break
        simulation.updateNests()

        # DRAW CURRENT MATRIX STATUSES
        for i in range(0, X_DIMENSION):
            for j in range(0, Y_DIMENSION):
                # order visually matters
                DrawRect((i * RECT_SIZE, j * RECT_SIZE), LerpColor(RED, simulation.getMToNestTrail()
                         [i][j])) if simulation.getMToNestTrail()[i][j] > 0 else None
                DrawRect((i * RECT_SIZE, j * RECT_SIZE), LerpColor(BLUE, simulation.getMToFoodTrail()
                         [i][j])) if simulation.getMToFoodTrail()[i][j] > 0 else None  # food trail
                DrawRect((i * RECT_SIZE, j * RECT_SIZE),
                         GREEN) if simulation.getMFoods()[i][j] > 0 else None  # food
                DrawRect((i * RECT_SIZE, j * RECT_SIZE),
                         WHITE) if simulation.getMAgents()[i][j] > 0 else None  # ant
                DrawRect((i * RECT_SIZE, j * RECT_SIZE),
                         YELLOW) if simulation.getMNests()[i][j] > 0 else None  # nest

                # trail evaporation
                simulation.getMToFoodTrail()[i][j] *= EVAPORATION_RATE
                simulation.getMToNestTrail()[i][j] *= EVAPORATION_RATE


        CLOCK.tick(CLOCK_SPEED)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
