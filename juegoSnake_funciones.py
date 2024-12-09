import pygame
import random
import sys
import os
import json
from pathlib import Path
from config import *
from juegoSnake_sonidos import play_sound, toggle_sound, is_sound_enabled

#Inicialización de la fuente
def get_font():
    return pygame.font.Font(None, 36)

#Función para dibujar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def load_rankings(file_path):
    if os.path.exists(file_path):  #Verifica si el archivo existe
        with open(file_path, "r") as file:
            return json.load(file)
    return []

#Función para guardar puntuaciones en rankings
def save_ranking(player_name, score):
    rankings = load_rankings(RANKINGS_FILE)  #Usa la función para cargar rankings
    rankings.append({"name": player_name, "score": score})
    rankings = sorted(rankings, key=lambda x: x["score"], reverse=True)[:10]  # Top 10
    with open(RANKINGS_FILE, "w") as file:
        json.dump(rankings, file)

#Función para mostrar rankings
def show_rankings(screen, clock):
    rankings = load_rankings(RANKINGS_FILE) #Usa la función para cargar rankings

    font = get_font()
    while True:
        screen.fill(NEGRO)
        draw_text("Rankings", font, BLANCO, screen, WIDTH // 2, 40)

        for i, entry in enumerate(rankings):
            name = entry.get('name', 'Nombre no disponible')
            score = entry.get('score', 'Puntaje no disponible')
            text = f"{i + 1}. {name}: {score}"
            draw_text(text, font, BLANCO, screen, WIDTH // 2, 80 + i * 30)

        draw_text("Presiona Esc para volver", font, BLANCO, screen, WIDTH // 2, HEIGHT - 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(15)

#Función para capturar el nombre del jugador
def get_player_name(screen, font):
    input_active = True
    player_name = ""
    while input_active:
        screen.fill(NEGRO)
        draw_text("Escribe tu nombre:", font, BLANCO, screen, WIDTH // 2, HEIGHT // 3)
        draw_text(player_name, font, VERDE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Presiona Enter para confirmar", font, BLANCO, screen, WIDTH // 2, HEIGHT - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 12:
                    player_name += event.unicode

        pygame.display.flip()

    return player_name if player_name else "Jugador"

#Función para el menú principal
def main_menu(screen, clock):
    font = get_font()
    while True:
        screen.fill(NEGRO)
        draw_text("Snake Game", font, BLANCO, screen, WIDTH // 2, HEIGHT // 3)
        draw_text("Presiona Enter para jugar", font, BLANCO, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Presiona R para ver rankings", font, BLANCO, screen, WIDTH // 2, HEIGHT // 2 + 40)
        draw_text("Presiona Esc para salir", font, BLANCO, screen, WIDTH // 2, HEIGHT // 2 + 80)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_r:
                    show_rankings(screen, clock)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(15)

#Función para el juego
def game(screen, clock):
    font = get_font()
    game_rect = pygame.Rect(60, 60, WIDTH - 120, HEIGHT - 120)
    snake = [(game_rect.left + 100, game_rect.top + 100), 
             (game_rect.left + 80, game_rect.top + 100), 
             (game_rect.left + 60, game_rect.top + 100)]
    direction = (CELL_SIZE, 0)
    food = (random.randint(game_rect.left // CELL_SIZE, (game_rect.right // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(game_rect.top // CELL_SIZE, (game_rect.bottom // CELL_SIZE) - 1) * CELL_SIZE)
    score = 0
    winning_score = 20

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
                if event.key == pygame.K_x:
                    toggle_sound()

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        if snake[0] == food:
            score += 1
            play_sound("juego/Sonidos/Snake_eat_fixed.wav")
            food = (random.randint(game_rect.left // CELL_SIZE, (game_rect.right // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(game_rect.top // CELL_SIZE, (game_rect.bottom // CELL_SIZE) - 1) * CELL_SIZE)
        else:
            snake.pop()

        if (new_head[0] < game_rect.left or new_head[0] >= game_rect.right or
                new_head[1] < game_rect.top or new_head[1] >= game_rect.bottom or
                new_head in snake[1:]):
            draw_text("¡Perdiste!", font, BLANCO, screen, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            player_name = get_player_name(screen, font)
            save_ranking(player_name, score)
            return

        if score >= winning_score:
            draw_text("¡Ganaste!", font, BLANCO, screen, WIDTH // 2, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            player_name = get_player_name(screen, font)
            save_ranking(player_name, score)
            return

        screen.fill(NEGRO)
        pygame.draw.rect(screen, MARRON, game_rect)
        pygame.draw.rect(screen, BLANCO, game_rect, 2)
        for segment in snake:
            pygame.draw.rect(screen, VERDE, (*segment, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, ROJO, (*food, CELL_SIZE, CELL_SIZE))
        draw_text(f"Score: {score}", font, BLANCO, screen, WIDTH - 100, 20)
        sound_status = "On" if is_sound_enabled() else "Off"
        draw_text(f"Sound: {sound_status} (X)", font, BLANCO, screen, WIDTH - 100, 50)

        pygame.display.flip()
        clock.tick(10)