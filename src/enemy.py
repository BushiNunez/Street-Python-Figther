"""Clase del enemigo con IA"""
import random
from src.character import Character
from src.constants import *

class Enemy(Character):
    """Enemigo controlado por IA"""
    
    def __init__(self, x, y):
        super().__init__(x, y, is_player=False)
        self.action_timer = 0
        
    def update(self, player):
        """Actualizar IA del enemigo"""
        super().update()
        self.action_timer -= 1
        
        if self.action_timer <= 0:
            self._decide_action(player)
            self.action_timer = random.randint(
                ENEMY_ACTION_MIN, ENEMY_ACTION_MAX
            )
    
    def _decide_action(self, player):
        """Decidir acción basada en distancia al jugador"""
        distance = abs(self.x - player.x)
        
        if distance > ENEMY_DISTANCE_CHASE:
            # Moverse hacia el jugador
            if self.x > player.x:
                self.move_left()
            else:
                self.move_right()
        else:
            # Estar cerca: atacar
            if random.random() > 0.6:
                if random.random() > 0.5:
                    self.punch()
                else:
                    self.kick()