"""Lógica principal del juego - REFACTORIZADA"""
import pygame
import random
from constants import *
from character import Character
from enemy import Enemy


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
        
        # Personajes con nombres de sprite
        self.player = Character(PLAYER_X, CHARACTER_Y, character_name="Green-snake", is_player=True)
        self.enemy = Enemy(ENEMY_X, CHARACTER_Y, character_name="Green-snake")  # Por ahora mismo color
        
        self.running = True
        self.game_over = False
        self.winner = None
        self.round_start = True
        self.round_start_timer = 120
        self.round_number = 1
        self.keys = {}
    
    def handle_input(self):
        """Manejar entrada del jugador y eventos de ventana"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keys[event.key] = True
            elif event.type == pygame.KEYUP:
                self.keys[event.key] = False
        
        # Manejo de controles del jugador (solo durante el juego)
        if not self.round_start and not self.game_over:
            # Movimiento
            if self.keys.get(pygame.K_LEFT, False) or self.keys.get(pygame.K_a, False):
                self.player.move_left()
            else:
                self.player.is_moving_left = False
            
            if self.keys.get(pygame.K_RIGHT, False) or self.keys.get(pygame.K_d, False):
                self.player.move_right()
            else:
                self.player.is_moving_right = False
            
            # Ataques
            if self.keys.get(pygame.K_z, False):
                self.player.punch()
            if self.keys.get(pygame.K_x, False):
                self.player.kick()
        
        # Reinicio del juego
        if self.game_over and self.keys.get(pygame.K_r, False):
            self.__init__()
    
    def check_collisions(self):
        """Detectar colisiones entre ataques y aplicar daño"""
        distance = abs(self.player.x - self.enemy.x)
        
        # Verificar ataque del jugador
        if self.player.is_attacking:
            player_range = PUNCH_RANGE if self.player.attack_type == 'punch' else KICK_RANGE
            
            # Verificar si está en rango
            if distance < player_range:
                # Verificar si está en la ventana activa (active frames del ataque)
                if self.player.attack_timer <= (PUNCH_TOTAL - PUNCH_STARTUP if self.player.attack_type == 'punch' else KICK_TOTAL - KICK_STARTUP):
                    if not self.player.attack_damage_dealt:
                        damage = PUNCH_DAMAGE if self.player.attack_type == 'punch' else KICK_DAMAGE
                        self.enemy.take_damage(damage)
                        self.player.attack_damage_dealt = True
                        print(f"¡Golpe del Jugador! Daño: {damage} | HP Enemigo: {int(self.enemy.health)}")
        
        # Verificar ataque del enemigo
        if self.enemy.is_attacking:
            enemy_range = PUNCH_RANGE if self.enemy.attack_type == 'punch' else KICK_RANGE
            
            if distance < enemy_range:
                # Verificar ventana activa del ataque enemigo
                if self.enemy.attack_timer <= (PUNCH_TOTAL - PUNCH_STARTUP if self.enemy.attack_type == 'punch' else KICK_TOTAL - KICK_STARTUP):
                    if not self.enemy.attack_damage_dealt:
                        damage = PUNCH_DAMAGE if self.enemy.attack_type == 'punch' else KICK_DAMAGE
                        self.player.take_damage(damage)
                        self.enemy.attack_damage_dealt = True
                        print(f"¡Golpe del Enemigo! Daño: {damage} | HP Jugador: {int(self.player.health)}")
    
    def update(self):
        """Actualizar lógica del juego"""
        if self.round_start:
            self.round_start_timer -= 1
            if self.round_start_timer <= 0:
                self.round_start = False
            return
        
        if self.game_over:
            return
        
        # Actualizar personajes
        self.player.update()
        self.enemy.update(self.player)
        
        # Actualizar direcciones de frente
        if self.enemy.x < self.player.x:
            self.player.facing_right = False
        else:
            self.player.facing_right = True
        
        if self.player.x < self.enemy.x:
            self.enemy.facing_right = True
        else:
            self.enemy.facing_right = False
        
        # Detectar colisiones
        self.check_collisions()
        
        # Verificar victoria/derrota
        if not self.player.is_alive():
            self.game_over = True
            self.winner = "ENEMY"
        elif not self.enemy.is_alive():
            self.game_over = True
            self.winner = "PLAYER"
    
    def draw(self):
        """Dibujar todo en pantalla"""
        self.screen.fill(DARK_BG)
        
        # Dibujar patrón de fondo
        for i in range(0, WINDOW_WIDTH, 120):
            pygame.draw.rect(self.screen, (30, 30, 50), (i, 0, 100, 120))
            pygame.draw.line(self.screen, (60, 60, 100), (i, 0), (i, 120), 2)
        
        # Línea central
        pygame.draw.line(self.screen, RED, (WINDOW_WIDTH // 2, 150), (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50), 3)
        
        # Dibujar personajes
        self.player.draw(self.screen)
        self.enemy.draw(self.screen)
        
        # Nombres de personajes
        player_name = self.font_medium.render("SNAKE-KYU", True, GREEN)
        self.screen.blit(player_name, (20, 15))
        
        enemy_name = self.font_medium.render("RATTLER", True, (255, 150, 0))
        self.screen.blit(enemy_name, (WINDOW_WIDTH - 250, 15))
        
        # Número de ronda
        round_text = self.font_large.render(f"ROUND {self.round_number}", True, RED)
        round_rect = round_text.get_rect(center=(WINDOW_WIDTH // 2, 35))
        self.screen.blit(round_text, round_rect)
        
        # Barras de vida
        bar_width = 280
        bar_height = 28
        
        # Barra del jugador (izquierda)
        pygame.draw.rect(self.screen, RED, (15, 90, bar_width, bar_height))
        fill = bar_width * (self.player.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, GREEN, (15, 90, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (15, 90, bar_width, bar_height), 3)
        
        player_hp = self.font_small.render(f"HP: {int(self.player.health)}", True, WHITE)
        self.screen.blit(player_hp, (30, 95))
        
        # Barra del enemigo (derecha)
        pygame.draw.rect(self.screen, RED, (WINDOW_WIDTH - 15 - bar_width, 90, bar_width, bar_height))
        fill = bar_width * (self.enemy.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, (255, 150, 0), (WINDOW_WIDTH - 15 - bar_width + (bar_width - fill), 90, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - 15 - bar_width, 90, bar_width, bar_height), 3)
        
        enemy_hp = self.font_small.render(f"HP: {int(self.enemy.health)}", True, WHITE)
        self.screen.blit(enemy_hp, (WINDOW_WIDTH - 30 - 100, 95))
        
        # Mostrar "FIGHT!" al inicio
        if self.round_start:
            fight = self.font_title.render("FIGHT!", True, RED)
            self.screen.blit(fight, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 40))
        
        # Pantalla de fin de juego
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
    
    def run(self):
        """Bucle principal del juego"""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()