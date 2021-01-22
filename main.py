import sys
import pygame
import constants
from city import City
from car import Car


def main(argv):
    city = City.read_file(argv[0])
    car1 = Car(constants.SIZE, 200, 0)

    carryOn = True
    pygame.init()
    size = (constants.WIDTH, constants.HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Traffic Simulator")
    while carryOn:
        screen.fill(constants.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
        city.display(screen)
        car1.display(screen)
        car1.move_down()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) == 0:
        argv.append("./examples/intersec_1.txt")
    main(argv)