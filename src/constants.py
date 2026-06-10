"""Constantes globales del juego"""
import pygame


# Ventana
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Street Python Fighter"
FPS = 60

# Posiciones iniciales
PLAYER_X = 200
ENEMY_X = 800
CHARACTER_Y = 400

# Estadísticas
HEALTH_MAX = 100
PUNCH_DAMAGE = 10
KICK_DAMAGE = 15
PUNCH_RANGE = 100
KICK_RANGE = 120

# Movimiento
MOVE_SPEED = 5
MOVE_RANGE_MIN = 50
MOVE_RANGE_MAX = WINDOW_WIDTH - 50

# IA
ENEMY_ACTION_MIN = 15
ENEMY_ACTION_MAX = 40
ENEMY_DISTANCE_CHASE = 200
ENEMY_DISTANCE_ATTACK = 100

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 255)
DARK_BG = (10, 14, 42)

# ANIMACIONES
ANIMATION_FRAME_SPEED = 6  # Cambiar frame cada N game frames (60/6 = 10 FPS para anims)
WALK_FRAMES = 6  # Número de frames en la animación de caminar
IDLE_FRAMES = 1  # Idle es una sola imagen
PUNCH_FRAMES = 1  # Punch es una sola imagen de ataque
KICK_FRAMES = 1  # Kick es una sola imagen de ataque

# FRAME DATA (Startup + Active + Recovery en frames de juego a 60 FPS)
PUNCH_STARTUP = 3
PUNCH_ACTIVE = 4
PUNCH_RECOVERY = 8
PUNCH_TOTAL = PUNCH_STARTUP + PUNCH_ACTIVE + PUNCH_RECOVERY

KICK_STARTUP = 6
KICK_ACTIVE = 5
KICK_RECOVERY = 10
KICK_TOTAL = KICK_STARTUP + KICK_ACTIVE + KICK_RECOVERY