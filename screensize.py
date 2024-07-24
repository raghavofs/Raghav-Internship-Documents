# import package pygame
import pygame

# initialize pygame
pygame.init()

# Form screen
screen = pygame.display.set_mode((750, 825), pygame.RESIZABLE)

# get the default size
x, y = screen.get_size()

# quit pygame
pygame.display.quit()

# view size (width x height)
print(x, y)
