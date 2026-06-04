"""Lógica principal del juego - Versión con imágenes PNG cargadas"""
import pygame
import random
import math
import os
import subprocess
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
        
        # Cargar o generar sprites
        self.load_sprites()
        
    def load_sprites(self):
        """Cargar sprites PNG desde archivos"""
        sprite_dir = 'assets/sprites'
        
        # Verificar si existen los sprites
        if not os.path.exists(f'{sprite_dir}/snake_green_idle.png'):
            print("Generando imágenes PNG de alta calidad...")
            print("Esto puede tomar un momento...")
            
            # Generar imágenes
            try:
                subprocess.run(['python3', 'assets/generate_images.py'], check=True)
                print("✅ Imágenes generadas correctamente")
            except:
                print("⚠️ No se pudieron generar las imágenes")
                print("Instala PIL: pip install Pillow --break-system-packages")
                return
        
        # Cargar sprites
        self.sprites = {}
        
        try:
            self.sprites['player_idle'] = pygame.image.load(f'{sprite_dir}/snake_green_idle.png').convert_alpha()
            self.sprites['player_punch'] = pygame.image.load(f'{sprite_dir}/snake_green_punch.png').convert_alpha()
            self.sprites['player_kick'] = pygame.image.load(f'{sprite_dir}/snake_green_kick.png').convert_alpha()
            
            self.sprites['enemy_idle'] = pygame.image.load(f'{sprite_dir}/snake_orange_idle.png').convert_alpha()
            self.sprites['enemy_punch'] = pygame.image.load(f'{sprite_dir}/snake_orange_punch.png').convert_alpha()
            self.sprites['enemy_kick'] = pygame.image.load(f'{sprite_dir}/snake_orange_kick.png').convert_alpha()
            
            print("✅ Sprites cargados correctamente")
        except Exception as e:
            print(f"Error cargando sprites: {e}")
    
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
                print(f"¡Golpe! Daño: {damage} | Distancia: {distance}")
            
        if self.enemy.is_attacking and distance < enemy_attack_range:
            if not self.enemy.attack_damage_dealt:
                damage = PUNCH_DAMAGE if self.enemy.attack_type == 'punch' else KICK_DAMAGE
                self.player.take_damage(damage)
                self.enemy.attack_damage_dealt = True
                print(f"¡Golpe enemigo! Daño: {damage} | Distancia: {distance}")
            
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
        
        if sprite is None:
            return
        
        x = int(character.x)
        y = int(character.y)
        
        if not character.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        rect = sprite.get_rect(center=(x, y))
        self.screen.blit(sprite, rect)
        
        # Aura de ataque
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