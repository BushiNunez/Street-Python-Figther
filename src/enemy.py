"""Clase del enemigo con IA - REFACTORIZADA"""
import random
from character import Character
from constants import (
    ENEMY_ACTION_MIN, ENEMY_ACTION_MAX,
    ENEMY_DISTANCE_CHASE, ENEMY_DISTANCE_ATTACK
)


class Enemy(Character):
    """Enemigo controlado por IA con soporte de animaciones"""
    
    def __init__(self, x, y, character_name="Green-snake"):
        super().__init__(x, y, character_name=character_name, is_player=False)
        self.action_timer = 0
    
    def update(self, player):
        """Actualizar IA del enemigo"""
        # Actualizar animación y estado general
        super().update()
        
        # Actualizar IA
        self.action_timer -= 1
        
        if self.action_timer <= 0:
            self._decide_action(player)
            self.action_timer = random.randint(ENEMY_ACTION_MIN, ENEMY_ACTION_MAX)
    
    def _decide_action(self, player):
        """Decidir acción basada en distancia al jugador"""
        distance = abs(self.x - player.x)
        
        # Si está lejos, acercarse
        if distance > ENEMY_DISTANCE_CHASE:
            if self.x > player.x:
                self.move_left()
            else:
                self.move_right()
        # Si está cerca, atacar
        elif random.random() > 0.6:
            if random.random() > 0.5:
                self.punch()
            else:
                self.kick()