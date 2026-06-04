"""Lógica principal del juego - Carga imágenes PNG"""
import pygame
import random
import math
from src.constants import *
from src.character import Character
from src.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 80)
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        self.player = Character(PLAYER_X, CHARACTER_Y, is_player=True)
        self.enemy = Enemy(ENEMY_X, CHARACTER_Y)
        
        self.running = True
        self.game_over = False
        self.winner = None
        self.animation_frame = 0
        self.round_start = True
        self.round_start_timer = 120
        self.round_number = 1
        self.keys = {}
        
        self.load_sprites()
    
    def load_sprites(self):
        """Cargar sprites PNG"""
        self.sprites = {}
        try:
            self.sprites['player_idle'] = pygame.image.load('assets/sprites/snake_green_idle.png').convert_alpha()
            self.sprites['player_punch'] = pygame.image.load('assets/sprites/snake_green_punch.png').convert_alpha()
            self.sprites['player_kick'] = pygame.image.load('assets/sprites/snake_green_kick.png').convert_alpha()
            self.sprites['enemy_idle'] = pygame.image.load('assets/sprites/snake_orange_idle.png').convert_alpha()
            self.sprites['enemy_punch'] = pygame.image.load('assets/sprites/snake_orange_punch.png').convert_alpha()
            self.sprites['enemy_kick'] = pygame.image.load('assets/sprites/snake_orange_kick.png').convert_alpha()
            print("✅ Sprites cargados correctamente")
        except Exception as e:
            print(f"❌ Error cargando sprites: {e}")
    
    def get_sprite(self, character, is_player):
        prefix = 'player' if is_player else 'enemy'
        if character.is_attacking:
            if character.attack_type == 'kick':
                return self.sprites.get(f'{prefix}_kick')
            else:
                return self.sprites.get(f'{prefix}_punch')
        return self.sprites.get(f'{prefix}_idle')
    
    def handle_input(self):
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
        distance = abs(self.player.x - self.enemy.x)
        player_range = PUNCH_RANGE if self.player.attack_type == 'punch' else KICK_RANGE
        enemy_range = PUNCH_RANGE if self.enemy.attack_type == 'punch' else KICK_RANGE
        
        if self.player.is_attacking and distance < player_range:
            if not self.player.attack_damage_dealt:
                damage = PUNCH_DAMAGE if self.player.attack_type == 'punch' else KICK_DAMAGE
                self.enemy.take_damage(damage)
                self.player.attack_damage_dealt = True
                print(f"¡Golpe! Daño: {damage}")
        
        if self.enemy.is_attacking and distance < enemy_range:
            if not self.enemy.attack_damage_dealt:
                damage = PUNCH_DAMAGE if self.enemy.attack_type == 'punch' else KICK_DAMAGE
                self.player.take_damage(damage)
                self.enemy.attack_damage_dealt = True
                print(f"¡Golpe enemigo! Daño: {damage}")
    
    def update(self):
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
        self.screen.fill(DARK_BG)
        
        for i in range(0, WINDOW_WIDTH, 120):
            pygame.draw.rect(self.screen, (30, 30, 50), (i, 0, 100, 120))
            pygame.draw.line(self.screen, (60, 60, 100), (i, 0), (i, 120), 2)
        
        pygame.draw.line(self.screen, RED, (WINDOW_WIDTH // 2, 150), (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50), 3)
        
        self.draw_character(self.player, True)
        self.draw_character(self.enemy, False)
        
        player_name = self.font_medium.render("SNAKE-KYU", True, GREEN)
        self.screen.blit(player_name, (20, 15))
        
        enemy_name = self.font_medium.render("RATTLER", True, (255, 150, 0))
        self.screen.blit(enemy_name, (WINDOW_WIDTH - 250, 15))
        
        round_text = self.font_large.render(f"ROUND {self.round_number}", True, RED)
        round_rect = round_text.get_rect(center=(WINDOW_WIDTH // 2, 35))
        self.screen.blit(round_text, round_rect)
        
        bar_width = 280
        bar_height = 28
        
        pygame.draw.rect(self.screen, RED, (15, 90, bar_width, bar_height))
        fill = bar_width * (self.player.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, GREEN, (15, 90, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (15, 90, bar_width, bar_height), 3)
        
        player_hp = self.font_small.render(f"HP: {int(self.player.health)}", True, WHITE)
        self.screen.blit(player_hp, (30, 95))
        
        pygame.draw.rect(self.screen, RED, (WINDOW_WIDTH - 15 - bar_width, 90, bar_width, bar_height))
        fill = bar_width * (self.enemy.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, (255, 150, 0), (WINDOW_WIDTH - 15 - bar_width + (bar_width - fill), 90, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - 15 - bar_width, 90, bar_width, bar_height), 3)
        
        enemy_hp = self.font_small.render(f"HP: {int(self.enemy.health)}", True, WHITE)
        self.screen.blit(enemy_hp, (WINDOW_WIDTH - 30 - 100, 95))
        
        if self.round_start:
            fight = self.font_title.render("FIGHT!", True, RED)
            self.screen.blit(fight, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 40))
        
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(190)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            result = self.font_large.render("¡VICTORY!" if self.winner == "PLAYER" else "GAME OVER", True, GREEN if self.winner == "PLAYER" else RED)
            restart = self.font_small.render("Presiona R para reiniciar", True, YELLOW)
            self.screen.blit(result, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 80))
            self.screen.blit(restart, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 80))
        
        pygame.display.flip()
    
    def draw_character(self, character, is_player):
        sprite = self.get_sprite(character, is_player)
        if not sprite:
            return
        
        x = int(character.x)
        y = int(character.y)
        
        if not character.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        rect = sprite.get_rect(center=(x, y))
        self.screen.blit(sprite, rect)
        
        if character.attack_timer > 5:
            pygame.draw.circle(self.screen, (255, 255, 0), (x, y), 130, 3)
    
    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
