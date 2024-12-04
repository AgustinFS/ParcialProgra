import pygame

#Control de sonido
sound_enabled = True

#Función para cargar y reproducir sonidos
def play_sound(file):
    global sound_enabled
    if sound_enabled:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

#Cambiar estado de sonido
def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled

#Verificar estado del sonido
def is_sound_enabled():
    return sound_enabled