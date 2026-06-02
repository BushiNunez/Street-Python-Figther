"""Clase base para personajes del juego"""
from src.constants import *

class Character:
    """Clase base para jugador y enemigo"""
    
    def __init__(self, x, y, color, is_player=True):
        self.x = x
        self.y = y
        self.color = color
        self.health = HEALTH_MAX
        self.is_attacking = False
        self.attack_type = None
        self.is_player = is_player
        self.facing_right = not is_player
        self.size = 40
        self.attack_timer = 0  # ← NUEVO: Contador para duración del ataque
        self.attack_damage_dealt = False  # ← NUEVO: Evitar daño múltiple
        
    def take_damage(self, damage):
        """Recibir daño"""
        self.health = max(0, self.health - damage)
        
    def punch(self):
        """Atacar con puño"""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_type = 'punch'
            self.attack_timer = 10  # ← NUEVO: Dura 10 frames (~500ms)
            self.attack_damage_dealt = False
    
    def kick(self):
        """Atacar con patada"""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_type = 'kick'
            self.attack_timer = 10  # ← NUEVO: Dura 10 frames (~500ms)
            self.attack_damage_dealt = False
            
    def move_left(self):
        """Mover a la izquierda"""
        self.x = max(MOVE_RANGE_MIN, self.x - MOVE_SPEED)
        self.facing_right = False
        
    def move_right(self):
        """Mover a la derecha"""
        self.x = min(MOVE_RANGE_MAX, self.x + MOVE_SPEED)
        self.facing_right = True
        
    def update(self):
        """Actualizar estado del personaje"""
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.attack_damage_dealt = False
            
    def is_alive(self):
        """Verificar si el personaje está vivo"""
        return self.health > 0