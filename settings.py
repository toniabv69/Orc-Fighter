import pygame

WIDTH, HEIGHT = 900, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 40
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
TITLE = "Orc Fighter"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
VERY_LIGHT_BLUE = (215, 215, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (125, 255, 125)
YELLOW = (200, 200, 50)
RED = (255, 0, 0)
LIGHT_BROWN = (196, 164, 132)

# reminder for health bar sizes:
# x must be multiple of 11
# y can be whatever
# coords and sizes:
# draw_healthbar(health, max_health, 20, 500, 440, 80)
# draw_healthbar(health, max_health, 440, 20, 440, 80)

FPS = 60
