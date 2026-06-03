"""Constantes globales del juego"""

# Ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Street Fighter - Python"
FPS = 20

# Posiciones iniciales
PLAYER_X = 100
ENEMY_X = 700
CHARACTER_Y = WINDOW_HEIGHT - 150

# Estadísticas de personajes
HEALTH_MAX = 100
PUNCH_DAMAGE = 10
KICK_DAMAGE = 15
PUNCH_RANGE = 80
KICK_RANGE = 100

# Movimiento
MOVE_SPEED = 15
MOVE_RANGE_MIN = 50
MOVE_RANGE_MAX = WINDOW_WIDTH - 50

# IA del enemigo
ENEMY_ACTION_MIN = 15
ENEMY_ACTION_MAX = 40
ENEMY_DISTANCE_CHASE = 150
ENEMY_DISTANCE_ATTACK = 80

# ========== ANIMACIÓN ==========
ANIMATION_SPEED = 5  # Velocidad de la animación (frames)
SNAKE_SEGMENTS = 5   # Cantidad de segmentos de la serpiente
SEGMENT_SIZE = 15    # Tamaño de cada segmento