import pygame
import sys
from juegoSnake_funciones import draw_text, main_menu, game

# Inicializar Pygame
pygame.init()

# Configuraciones principales
WIDTH, HEIGHT = 600, 400
BLACK = (0, 0, 0)

# Inicializar pantalla y reloj
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Bucle principal
while True:
    main_menu(screen, clock)
    game(screen, clock)