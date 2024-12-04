import pygame
import sys
from juegoSnake_funciones import main_menu, game, WIDTH, HEIGHT

#Inicializar Pygame
pygame.init()


#Inicializar pantalla y reloj
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

#Bucle principal
while True:
    main_menu(screen, clock)
    game(screen, clock)