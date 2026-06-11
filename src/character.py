"""Clase base para personajes del juego - CON COLISIONES Y HITBOX"""
import pygame
from constants import (
    HEALTH_MAX, MOVE_SPEED, MOVE_RANGE_MIN, MOVE_RANGE_MAX,
    PUNCH_DAMAGE, KICK_DAMAGE, PUNCH_TOTAL, KICK_TOTAL
)
from animation import AnimationController


class Character:
    """Clase base para jugador y enemigo con soporte de animaciones y colisiones"""
    
    def __init__(self, x, y, character_name="Green-snake", is_player=True):
        """
        Inicializar un personaje.
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            character_name: Nombre del personaje para cargar sprites
            is_player: Si es el jugador o la IA
        """
        self.x = x
        self.y = y
        self.health = HEALTH_MAX
        self.is_player = is_player
        self.facing_right = not is_player
        
        # Estados de ataque
        self.is_attacking = False
        self.attack_type = None
        self.attack_timer = 0
        self.attack_damage_dealt = False
        
        # Estado de movimiento
        self.is_moving_left = False
        self.is_moving_right = False
        
        # Dimensiones (tamaño de la hitbox para colisiones)
        self.width = 80      # Ancho de la hitbox (más estrecho que el sprite visual)
        self.height = 100    # Alto de la hitbox
        
        # Animaciones
        self.animation_controller = AnimationController(character_name)
        self.current_state = 'idle'
    
    def get_hitbox_rect(self):
        """
        Obtener el rectángulo de colisión (hitbox) del personaje.
        
        Returns:
            pygame.Rect centrado en la posición del personaje
        """
        return pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
    
    def can_move_to(self, new_x, other_character=None):
        """
        Verificar si el personaje puede moverse a una nueva posición X.
        
        Args:
            new_x: Nueva posición X
            other_character: Otro personaje para detectar colisión
            
        Returns:
            True si puede moverse, False si hay colisión
        """
        # Verificar límites de pantalla
        if new_x < MOVE_RANGE_MIN or new_x > MOVE_RANGE_MAX:
            return False
        
        # Verificar colisión con otro personaje
        if other_character:
            # Crear rect hipotético del movimiento
            temp_rect = pygame.Rect(
                new_x - self.width // 2,
                self.y - self.height // 2,
                self.width,
                self.height
            )
            
            # Obtener rect del otro personaje
            other_rect = other_character.get_hitbox_rect()
            
            # Si se solapan, no permitir movimiento
            if temp_rect.colliderect(other_rect):
                return False
        
        return True
    
    def _get_current_state(self):
        """Determinar el estado actual del personaje para animación"""
        if self.is_attacking:
            if self.attack_type == 'punch':
                return 'punch'
            elif self.attack_type == 'kick':
                return 'kick'
        elif self.is_moving_left or self.is_moving_right:
            return 'walk'
        else:
            return 'idle'
    
    def take_damage(self, damage):
        """Recibir daño"""
        self.health = max(0, self.health - damage)
    
    def punch(self):
        """Atacar con puño"""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_type = 'punch'
            self.attack_timer = PUNCH_TOTAL
            self.attack_damage_dealt = False
            self.animation_controller.reset_animation()
    
    def kick(self):
        """Atacar con patada"""
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_type = 'kick'
            self.attack_timer = KICK_TOTAL
            self.attack_damage_dealt = False
            self.animation_controller.reset_animation()
    
    def move_left(self):
        """Mover a la izquierda (sin validación - se valida en Game)"""
        self.x = max(MOVE_RANGE_MIN, self.x - MOVE_SPEED)
        self.facing_right = False
        self.is_moving_left = True
    
    def move_right(self):
        """Mover a la derecha (sin validación - se valida en Game)"""
        self.x = min(MOVE_RANGE_MAX, self.x + MOVE_SPEED)
        self.facing_right = True
        self.is_moving_right = True
    
    def stop_moving(self):
        """Detener el movimiento (para limpiar flags)"""
        self.is_moving_left = False
        self.is_moving_right = False
    
    def update(self):
        """Actualizar estado del personaje y animación"""
        # Actualizar timer de ataque
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.attack_damage_dealt = False
        
        # Actualizar estado actual
        new_state = self._get_current_state()
        
        # Si cambió el estado, resetear animación
        if new_state != self.current_state:
            self.current_state = new_state
            self.animation_controller.reset_animation()
        
        # Actualizar frames de animación
        self.animation_controller.update()
    
    def get_sprite(self):
        """
        Obtener el sprite actual basado en el estado.
        
        Returns:
            pygame.Surface con la imagen del personaje
        """
        return self.animation_controller.get_frame(
            self.current_state,
            facing_right=self.facing_right
        )
    
    def is_alive(self):
        """Verificar si el personaje está vivo"""
        return self.health > 0
    
    def draw(self, screen, debug=False):
        """
        Dibujar el personaje en pantalla.
        
        Args:
            screen: Superficie de Pygame donde dibujar
            debug: Si True, dibuja la hitbox para debug
        """
        sprite = self.get_sprite()
        if sprite is None:
            return
        
        # Obtener rect y dibujar
        rect = sprite.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(sprite, rect)
        """
        # Debug: mostrar hitbox cuando está atacando
        if self.is_attacking and self.attack_timer > 5:
            pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 130, 3)
        
        # Debug: mostrar hitbox de colisión
     
            if debug:
            hitbox = self.get_hitbox_rect()
            pygame.draw.rect(screen, (255, 0, 0), hitbox, 2)
        """