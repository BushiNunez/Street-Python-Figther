"""Lógica principal del juego - Versión con sprites PNG auto-generados"""
import pygame
import random
import math
import os
from src.constants import *
from src.character import Character
from src.enemy import Enemy

class Game:
    """Clase principal que controla la lógica del juego"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 80)
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Personajes
        self.player = Character(PLAYER_X, CHARACTER_Y, is_player=True)
        self.enemy = Enemy(ENEMY_X, CHARACTER_Y)
        
        # Estado del juego
        self.running = True
        self.game_over = False
        self.winner = None
        self.animation_frame = 0
        self.round_start = True
        self.round_start_timer = 120
        self.round_number = 1
        
        # Controles
        self.keys = {}
        
        # Generar sprites
        self.generate_all_sprites()
        
    def create_snake_sprite(self, width=150, height=180, color_scheme='green'):
        """Crear sprite de serpiente"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        if color_scheme == 'green':
            main = (102, 221, 0)
            dark = (51, 153, 0)
            accent = (255, 0, 0)
        else:
            main = (255, 153, 0)
            dark = (204, 102, 0)
            accent = (0, 100, 255)
        
        cx, cy = width // 2, height // 2
        
        # Cuerpo
        pygame.draw.ellipse(surface, (220, 220, 180), (cx - 35, cy - 10, 70, 90))
        pygame.draw.ellipse(surface, main, (cx - 50, cy - 15, 45, 100))
        pygame.draw.ellipse(surface, main, (cx + 5, cy - 15, 45, 100))
        
        # Músculos
        pygame.draw.line(surface, dark, (cx - 40, cy + 10), (cx - 20, cy + 10), 3)
        pygame.draw.line(surface, dark, (cx - 40, cy + 35), (cx - 20, cy + 35), 3)
        pygame.draw.line(surface, dark, (cx - 40, cy + 60), (cx - 20, cy + 60), 3)
        pygame.draw.line(surface, dark, (cx + 20, cy + 10), (cx + 40, cy + 10), 3)
        pygame.draw.line(surface, dark, (cx + 20, cy + 35), (cx + 40, cy + 35), 3)
        pygame.draw.line(surface, dark, (cx + 20, cy + 60), (cx + 40, cy + 60), 3)
        
        # Cinturón
        pygame.draw.rect(surface, accent, (cx - 40, cy + 60, 80, 15))
        pygame.draw.rect(surface, (0, 0, 0), (cx - 40, cy + 60, 80, 15), 2)
        
        # Piernas
        pygame.draw.ellipse(surface, main, (cx - 55, cy + 70, 22, 40))
        pygame.draw.ellipse(surface, dark, (cx - 55, cy + 70, 22, 40), 2)
        pygame.draw.circle(surface, dark, (cx - 44, cy + 110), 9)
        pygame.draw.polygon(surface, dark, [(cx - 50, cy + 110), (cx - 44, cy + 120), (cx - 38, cy + 110)])
        
        pygame.draw.ellipse(surface, main, (cx + 33, cy + 70, 22, 40))
        pygame.draw.ellipse(surface, dark, (cx + 33, cy + 70, 22, 40), 2)
        pygame.draw.circle(surface, dark, (cx + 44, cy + 110), 9)
        pygame.draw.polygon(surface, dark, [(cx + 38, cy + 110), (cx + 44, cy + 120), (cx + 50, cy + 110)])
        
        # Brazos
        pygame.draw.circle(surface, main, (cx - 55, cy + 15), 11)
        pygame.draw.line(surface, main, (cx - 55, cy + 15), (cx - 70, cy + 30), 15)
        pygame.draw.circle(surface, dark, (cx - 70, cy + 30), 12)
        pygame.draw.circle(surface, (150, 150, 150), (cx - 70, cy + 30), 8)
        
        pygame.draw.circle(surface, main, (cx + 55, cy + 15), 11)
        pygame.draw.line(surface, main, (cx + 55, cy + 15), (cx + 70, cy + 30), 15)
        pygame.draw.circle(surface, dark, (cx + 70, cy + 30), 12)
        pygame.draw.circle(surface, (150, 150, 150), (cx + 70, cy + 30), 8)
        
        # Cuello
        pygame.draw.ellipse(surface, main, (cx - 25, cy - 50, 50, 35))
        pygame.draw.ellipse(surface, dark, (cx - 25, cy - 50, 50, 35), 2)
        
        # Cabeza
        head_y = cy - 100
        
        pygame.draw.ellipse(surface, main, (cx - 45, head_y - 25, 90, 65))
        pygame.draw.ellipse(surface, dark, (cx - 45, head_y - 25, 90, 65), 3)
        
        pygame.draw.polygon(surface, main, [(cx - 35, head_y + 35), (cx + 35, head_y + 35), (cx + 38, head_y + 48), (cx - 38, head_y + 48)])
        pygame.draw.polygon(surface, (220, 220, 180), [(cx - 25, head_y + 24), (cx + 25, head_y + 24), (cx + 22, head_y + 38), (cx - 22, head_y + 38)])
        
        pygame.draw.polygon(surface, (255, 255, 255), [(cx - 15, head_y + 24), (cx - 20, head_y + 42), (cx - 10, head_y + 32)])
        pygame.draw.polygon(surface, (255, 255, 255), [(cx + 15, head_y + 24), (cx + 20, head_y + 42), (cx + 10, head_y + 32)])
        
        pygame.draw.line(surface, dark, (cx - 40, head_y - 5), (cx - 15, head_y + 10), 3)
        pygame.draw.line(surface, dark, (cx + 40, head_y - 5), (cx + 15, head_y + 10), 3)
        
        # Ojos
        pygame.draw.ellipse(surface, (255, 255, 0), (cx - 20, head_y - 15, 26, 18))
        pygame.draw.ellipse(surface, (0, 0, 0), (cx - 16, head_y - 11, 12, 10))
        pygame.draw.circle(surface, (255, 255, 0), (cx - 12, head_y - 8), 3)
        
        pygame.draw.ellipse(surface, (255, 255, 0), (cx - 6, head_y - 15, 26, 18))
        pygame.draw.ellipse(surface, (0, 0, 0), (cx - 2, head_y - 11, 12, 10))
        pygame.draw.circle(surface, (255, 255, 0), (cx + 2, head_y - 8), 3)
        
        pygame.draw.polygon(surface, dark, [(cx, head_y - 2), (cx - 5, head_y + 5), (cx + 5, head_y + 5)])
        
        # Cresta
        crest_y = head_y - 28
        for i in range(5):
            crest_x = cx - 30 + (i * 15)
            pygame.draw.polygon(surface, accent, [(crest_x, crest_y), (crest_x - 8, crest_y - 20), (crest_x + 8, crest_y - 20)])
            pygame.draw.line(surface, (0, 0, 0), (crest_x - 8, crest_y - 20), (crest_x + 8, crest_y - 20), 2)
        
        return surface
    
    def create_punch_sprite(self, width=150, height=180, color_scheme='green'):
        """Crear sprite de serpiente con puño extendido"""
        surface = self.create_snake_sprite(width, height, color_scheme)
        
        if color_scheme == 'green':
            main = (102, 221, 0)
            dark = (51, 153, 0)
        else:
            main = (255, 153, 0)
            dark = (204, 102, 0)
        
        cx, cy = width // 2, height // 2
        
        pygame.draw.line(surface, main, (cx + 55, cy + 15), (cx + 90, cy + 35), 18)
        pygame.draw.circle(surface, dark, (cx + 90, cy + 35), 14)
        pygame.draw.circle(surface, (150, 150, 150), (cx + 90, cy + 35), 10)
        
        return surface
    
    def create_kick_sprite(self, width=150, height=180, color_scheme='green'):
        """Crear sprite de serpiente pateando"""
        surface = self.create_snake_sprite(width, height, color_scheme)
        
        if color_scheme == 'green':
            main = (102, 221, 0)
            dark = (51, 153, 0)
        else:
            main = (255, 153, 0)
            dark = (204, 102, 0)
        
        cx, cy = width // 2, height // 2
        
        pygame.draw.ellipse(surface, main, (cx + 35, cy + 65, 20, 50))
        pygame.draw.ellipse(surface, dark, (cx + 35, cy + 65, 20, 50), 2)
        pygame.draw.circle(surface, dark, (cx + 45, cy + 115), 11)
        pygame.draw.polygon(surface, dark, [(cx + 40, cy + 115), (cx + 45, cy + 130), (cx + 50, cy + 115)])
        
        return surface
    
    def generate_all_sprites(self):
        """Generar todos los sprites en memoria"""
        print("Generando sprites...")
        
        self.sprites = {
            'player_idle': self.create_snake_sprite(150, 180, 'green'),
            'player_punch': self.create_punch_sprite(150, 180, 'green'),
            'player_kick': self.create_kick_sprite(150, 180, 'green'),
            'enemy_idle': self.create_snake_sprite(150, 180, 'orange'),
            'enemy_punch': self.create_punch_sprite(150, 180, 'orange'),
            'enemy_kick': self.create_kick_sprite(150, 180, 'orange'),
        }
        
        print("✅ Sprites generados en memoria")
    
    def get_sprite(self, character, is_player):
        """Obtener sprite correcto según estado"""
        prefix = 'player' if is_player else 'enemy'
        
        if character.is_attacking:
            if character.attack_type == 'kick':
                return self.sprites.get(f'{prefix}_kick', self.sprites.get(f'{prefix}_idle'))
            else:
                return self.sprites.get(f'{prefix}_punch', self.sprites.get(f'{prefix}_idle'))
        
        return self.sprites.get(f'{prefix}_idle')
    
    def handle_input(self):
        """Procesar entrada"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keys[event.key] = True
            elif event.type == pygame.KEYUP:
                self.keys[event.key] = False
        
        if not self.round_start and not self.game_over:
            if self.keys.get(pygame.K_LEFT, False) or self.keys.get(pygame.K_a, False):
                self.player.move_left()
            if self.keys.get(pygame.K_RIGHT, False) or self.keys.get(pygame.K_d, False):
                self.player.move_right()
            if self.keys.get(pygame.K_z, False):
                self.player.punch()
            if self.keys.get(pygame.K_x, False):
                self.player.kick()
            
        if self.game_over and self.keys.get(pygame.K_r, False):
            self.__init__()
            
    def check_collisions(self):
        """Verificar si los ataques conectan"""
        distance = abs(self.player.x - self.enemy.x)
        
        player_attack_range = PUNCH_RANGE if self.player.attack_type == 'punch' else KICK_RANGE
        enemy_attack_range = PUNCH_RANGE if self.enemy.attack_type == 'punch' else KICK_RANGE
        
        if self.player.is_attacking and distance < player_attack_range:
            if not self.player.attack_damage_dealt:
                damage = PUNCH_DAMAGE if self.player.attack_type == 'punch' else KICK_DAMAGE
                self.enemy.take_damage(damage)
                self.player.attack_damage_dealt = True
                print(f"¡Golpe del jugador! Daño: {damage}")
            
        if self.enemy.is_attacking and distance < enemy_attack_range:
            if not self.enemy.attack_damage_dealt:
                damage = PUNCH_DAMAGE if self.enemy.attack_type == 'punch' else KICK_DAMAGE
                self.player.take_damage(damage)
                self.enemy.attack_damage_dealt = True
                print(f"¡Golpe del enemigo! Daño: {damage}")
            
    def update(self):
        """Actualizar lógica"""
        if self.round_start:
            self.round_start_timer -= 1
            if self.round_start_timer <= 0:
                self.round_start = False
            return
            
        if self.game_over:
            return
            
        self.player.update()
        self.enemy.update(self.player)
        
        if self.enemy.x < self.player.x:
            self.player.facing_right = False
        else:
            self.player.facing_right = True
            
        if self.player.x < self.enemy.x:
            self.enemy.facing_right = True
        else:
            self.enemy.facing_right = False
        
        self.check_collisions()
        self.animation_frame += 1
        
        if not self.player.is_alive():
            self.game_over = True
            self.winner = "ENEMY"
        elif not self.enemy.is_alive():
            self.game_over = True
            self.winner = "PLAYER"
    
    def draw(self):
        """Dibujar pantalla"""
        self.screen.fill(DARK_BG)
        
        # Fondo
        for i in range(0, WINDOW_WIDTH, 120):
            pygame.draw.rect(self.screen, (30, 30, 50), (i, 0, 100, 120))
            pygame.draw.line(self.screen, (60, 60, 100), (i, 0), (i, 120), 2)
            for j in range(0, 120, 25):
                pygame.draw.rect(self.screen, (80, 80, 120), (i + 8, j + 8, 15, 15))
                pygame.draw.rect(self.screen, (40, 40, 80), (i + 10, j + 10, 10, 10))
        
        # Línea divisoria
        pygame.draw.line(self.screen, RED, 
                        (WINDOW_WIDTH // 2, 150), 
                        (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50), 3)
        
        # Personajes
        self.draw_sprite_character(self.player, True)
        self.draw_sprite_character(self.enemy, False)
        
        # UI
        player_name = self.font_medium.render("SNAKE-KYU", True, GREEN)
        self.screen.blit(player_name, (20, 15))
        
        enemy_name = self.font_medium.render("RATTLER", True, (255, 150, 0))
        enemy_name_rect = enemy_name.get_rect()
        self.screen.blit(enemy_name, (WINDOW_WIDTH - enemy_name_rect.width - 20, 15))
        
        round_text = self.font_large.render(f"ROUND {self.round_number}", True, RED)
        round_rect = round_text.get_rect(center=(WINDOW_WIDTH // 2, 35))
        self.screen.blit(round_text, round_rect)
        
        # HP Bars
        bar_width = 280
        bar_height = 28
        
        pygame.draw.rect(self.screen, RED, (15, 90, bar_width, bar_height))
        fill = bar_width * (self.player.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, GREEN, (15, 90, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (15, 90, bar_width, bar_height), 3)
        
        player_hp_text = self.font_small.render(f"{int(self.player.health)}/{HEALTH_MAX}", True, WHITE)
        self.screen.blit(player_hp_text, (30, 95))
        
        pygame.draw.rect(self.screen, RED, (WINDOW_WIDTH - 15 - bar_width, 90, bar_width, bar_height))
        fill = bar_width * (self.enemy.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, (255, 150, 0), 
                        (WINDOW_WIDTH - 15 - bar_width + (bar_width - fill), 90, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - 15 - bar_width, 90, bar_width, bar_height), 3)
        
        enemy_hp_text = self.font_small.render(f"{int(self.enemy.health)}/{HEALTH_MAX}", True, WHITE)
        enemy_hp_rect = enemy_hp_text.get_rect()
        self.screen.blit(enemy_hp_text, (WINDOW_WIDTH - 30 - enemy_hp_rect.width, 95))
        
        if self.round_start:
            fight_text = self.font_title.render("FIGHT!", True, RED)
            text_rect = fight_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(fight_text, text_rect)
        
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(190)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            if self.winner == "PLAYER":
                result = self.font_large.render("¡VICTORY!", True, GREEN)
            else:
                result = self.font_large.render("GAME OVER", True, RED)
            
            restart = self.font_small.render("Presiona R para reiniciar", True, YELLOW)
            
            result_rect = result.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
            restart_rect = restart.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            
            self.screen.blit(result, result_rect)
            self.screen.blit(restart, restart_rect)
        
        pygame.display.flip()
    
    def draw_sprite_character(self, character, is_player):
        """Dibujar personaje con sprite"""
        sprite = self.get_sprite(character, is_player)
        
        x = int(character.x)
        y = int(character.y)
        
        if not character.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        rect = sprite.get_rect(center=(x, y))
        self.screen.blit(sprite, rect)
        
        if character.attack_timer > 5:
            aura_radius = 130 + (self.animation_frame % 10) * 2
            pygame.draw.circle(self.screen, (255, 255, 0), (x, y), aura_radius, 3)
        
    def run(self):
        """Loop principal"""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()