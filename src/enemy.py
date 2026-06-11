"""Clase del enemigo con IA mejorada - Mira y golpea hacia el jugador"""
import random
from character import Character
from constants import (
    ENEMY_ACTION_MIN, ENEMY_ACTION_MAX,
    ENEMY_DISTANCE_CHASE, ENEMY_DISTANCE_ATTACK
)


class Enemy(Character):
    """Enemigo controlado por IA inteligente"""
    
    def __init__(self, x, y, character_name="Green-snake"):
        super().__init__(x, y, character_name=character_name, is_player=False)
        self.action_timer = 0
    
    def update(self, player):
        """Actualizar IA del enemigo"""
        # Actualizar animación y estado general
        super().update()
        
        # ✅ IMPORTANTE: Actualizar dirección hacia el jugador SIEMPRE
        if player.x < self.x:
            self.facing_right = False
        else:
            self.facing_right = True
        
        # Actualizar IA
        self.action_timer -= 1
        
        if self.action_timer <= 0:
            self._decide_action(player)
            self.action_timer = random.randint(ENEMY_ACTION_MIN, ENEMY_ACTION_MAX)
    
    def _decide_action(self, player):
        """Decidir acción basada en distancia y dirección al jugador"""
        distance = abs(self.x - player.x)
        
        # Determinar si el enemigo está mirando hacia el jugador
        enemy_looking_right = self.facing_right
        player_is_to_right = player.x > self.x
        
        # ✅ El enemigo está mirando HACIA el jugador
        is_facing_player = (enemy_looking_right and player_is_to_right) or \
                          (not enemy_looking_right and not player_is_to_right)
        
        # Si está lejos, acercarse
        if distance > ENEMY_DISTANCE_CHASE:
            if self.x > player.x:
                self.move_left()
            else:
                self.move_right()
        
        # Si está cerca Y está mirando hacia el jugador, atacar
        elif distance < ENEMY_DISTANCE_ATTACK and is_facing_player:
            if random.random() > 0.6:  # 40% de probabilidad de atacar
                if random.random() > 0.5:
                    self.punch()
                else:
                    self.kick()
        
        # Si está cerca pero NO está mirando, moverse para girar
        elif distance < ENEMY_DISTANCE_CHASE and not is_facing_player:
            # Intentar acercarse un poco más para cambiar posición
            if self.x > player.x:
                self.move_left()
            else:
                self.move_right()