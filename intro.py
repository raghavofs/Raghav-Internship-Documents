import pygame
import sys


pygame.init()


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Example")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

x, y = 400, 300
radius = 50
speed = 5


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    x += speed
    if x > 800 - radius or x < radius:
        speed = -speed


    screen.fill(WHITE)


    pygame.draw.circle(screen, RED, (x, y), radius)


    pygame.display.flip()


    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
