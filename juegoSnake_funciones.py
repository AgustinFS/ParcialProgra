import pygame
import random
import sys
from juegoSnake_sonidos import play_sound, toggle_sound, is_sound_enabled

# Configuraciones principales
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Inicialización de fuente
def get_font():
    return pygame.font.Font(None, 36)

# Función para mostrar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Menú principal
def main_menu(screen, clock):
    font = get_font()  # Inicializa la fuente de texto
    while True:
        screen.fill(BLACK)
        draw_text("Snake Game", font, WHITE, screen, WIDTH // 2, HEIGHT // 3)
        draw_text("Presiona Enter para jugar", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Presiona Esc para salir", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Salir del menú y empieza el juego
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(15)

# Parte principal del juegouego principal
def game(screen, clock):
    font = get_font()  # Inicializa la fuente aquí
    # Variables del juego
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)  # Derecha
    food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
    score = 0
    winning_score = 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                if event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                if event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                if event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
                if event.key == pygame.K_x:  # Tecla para silenciar/activar sonido
                    toggle_sound()

        # Mover la serpiente
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        # Verificar si la serpiente come la comida
        if snake[0] == food:
            score += 1
            play_sound("juego/Sonidos/Snake_eat_fixed.wav")
            food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        #else:
            #snake.pop()  # Eliminar la última parte de la serpiente si no come

        # Verificar colisiones
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake[1:]):
            #play_sound("juego/Sonidos/lose.mp3")
            draw_text("¡Perdiste!", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            return  # Regresar al menú principal

        # Verificar victoria
        if score >= winning_score:
            #play_sound("juego/Sonidos/win.mp3")
            draw_text("¡Ganaste!", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            return  # Regresar al menú principal

        # Dibujar todo
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

        # Mostrar puntuación
        draw_text(f"Score: {score}", font, WHITE, screen, WIDTH // 2, 20)
        sound_status = "On" if is_sound_enabled() else "Off"
        draw_text(f"Sound: {sound_status} (X)", font, WHITE, screen, WIDTH - 100, 20)

        pygame.display.flip()
        clock.tick(10)