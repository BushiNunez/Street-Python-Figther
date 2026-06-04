"""Lógica principal del juego con Pygame"""
import pygame
import random
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
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Personajes
        self.player = Character(PLAYER_X, CHARACTER_Y, is_player=True)
        self.enemy = Enemy(ENEMY_X, CHARACTER_Y)
        
        # Estado del juego
        self.running = True
        self.game_over = False
        self.winner = None
        self.animation_frame = 0
        self.round_start = True
        self.round_start_timer = 120  # 2 segundos a 60 FPS
        
        # Controles
        self.keys = {}
        
    def handle_input(self):
        """Procesar entrada"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keys[event.key] = True
            elif event.type == pygame.KEYUP:
                self.keys[event.key] = False
        
        # Movimiento
        if self.keys.get(pygame.K_LEFT, False) or self.keys.get(pygame.K_a, False):
            self.player.move_left()
        if self.keys.get(pygame.K_RIGHT, False) or self.keys.get(pygame.K_d, False):
            self.player.move_right()
            
        # Ataques
        if self.keys.get(pygame.K_z, False):
            self.player.punch()
        if self.keys.get(pygame.K_x, False):
            self.player.kick()
            
        # Reiniciar
        if self.game_over and self.keys.get(pygame.K_r, False):
            self.__init__()
            
    def check_collisions(self):
        """Verificar si los ataques conectan"""
        distance = abs(self.player.x - self.enemy.x)
        
        # Ataque del jugador
        if self.player.is_attacking and distance < PUNCH_RANGE:
            if not self.player.attack_damage_dealt:
                damage = PUNCH_DAMAGE if self.player.attack_type == 'punch' else KICK_DAMAGE
                self.enemy.take_damage(damage)
                self.player.attack_damage_dealt = True
                print(f"¡Golpe! Daño: {damage}")
            
        # Ataque del enemigo
        if self.enemy.is_attacking and distance < PUNCH_RANGE:
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
        self.check_collisions()
        self.animation_frame += 1
        
        # Verificar victoria
        if not self.player.is_alive():
            self.game_over = True
            self.winner = "ENEMY"
        elif not self.enemy.is_alive():
            self.game_over = True
            self.winner = "PLAYER"
            
    def draw_snake(self, character, is_player):
        """Dibujar serpiente"""
        x = int(character.x)
        y = int(character.y)
        
        # Colores según personaje
        if is_player:
            main_color = (102, 221, 0)      # Verde
            dark_color = (51, 153, 0)       # Verde oscuro
            accent = (255, 0, 0)            # Rojo
        else:
            main_color = (255, 153, 0)      # Naranja
            dark_color = (204, 102, 0)      # Naranja oscuro
            accent = (0, 100, 255)          # Azul
        
        # Cuerpo
        pygame.draw.ellipse(self.screen, main_color, 
                          (x - 40, y - 40, 80, 100))
        
        # Cabeza
        pygame.draw.circle(self.screen, main_color, (x, y - 60), 35)
        
        # Ojos
        eye_offset = 15
        pygame.draw.circle(self.screen, (255, 255, 0), (x - eye_offset, y - 70), 6)
        pygame.draw.circle(self.screen, (255, 255, 0), (x + eye_offset, y - 70), 6)
        pygame.draw.circle(self.screen, (0, 0, 0), (x - eye_offset, y - 70), 3)
        pygame.draw.circle(self.screen, (0, 0, 0), (x + eye_offset, y - 70), 3)
        
        # Boca
        pygame.draw.line(self.screen, (255, 200, 0), (x - 15, y - 50), (x + 15, y - 50), 3)
        
        # Brazos
        arm_y = y - 20
        pygame.draw.ellipse(self.screen, main_color, (x - 70, arm_y - 15, 30, 30))
        pygame.draw.ellipse(self.screen, main_color, (x + 40, arm_y - 15, 30, 30))
        
        # Puños
        pygame.draw.circle(self.screen, dark_color, (x - 75, arm_y), 15)
        pygame.draw.circle(self.screen, dark_color, (x + 75, arm_y), 15)
        
        # Cola
        for i in range(5):
            tail_x = x - 50 - (i * 25)
            tail_y = y + 30 + (5 * (i % 2))
            pygame.draw.circle(self.screen, main_color, (tail_x, tail_y), 12 - i)
        
        # Cinturón
        pygame.draw.rect(self.screen, accent, (x - 45, y + 35, 90, 15))
        
        # Aura de ataque
        if character.attack_timer > 5:
            pygame.draw.circle(self.screen, (255, 255, 0), (x, y), 100, 3)
            
    def draw(self):
        """Dibujar pantalla"""
        self.screen.fill(DARK_BG)
        
        # Línea divisoria
        pygame.draw.line(self.screen, RED, 
                        (WINDOW_WIDTH // 2, 50), 
                        (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50), 2)
        
        # Personajes
        self.draw_snake(self.player, True)
        self.draw_snake(self.enemy, False)
        
        # Nombres
        player_text = self.font_small.render("SNAKE-KYU", True, GREEN)
        enemy_text = self.font_small.render("RATTLER", True, (255, 150, 0))
        self.screen.blit(player_text, (50, 20))
        self.screen.blit(enemy_text, (WINDOW_WIDTH - 250, 20))
        
        # Salud
        player_hp = self.font_small.render(f"HP: {int(self.player.health)}", True, GREEN)
        enemy_hp = self.font_small.render(f"HP: {int(self.enemy.health)}", True, (255, 150, 0))
        self.screen.blit(player_hp, (50, 70))
        self.screen.blit(enemy_hp, (WINDOW_WIDTH - 250, 70))
        
        # Barra de salud jugador
        bar_width = 200
        bar_height = 20
        pygame.draw.rect(self.screen, RED, (50, 120, bar_width, bar_height))
        fill = bar_width * (self.player.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, GREEN, (50, 120, fill, bar_height))
        
        # Barra de salud enemigo
        pygame.draw.rect(self.screen, RED, (WINDOW_WIDTH - 250, 120, bar_width, bar_height))
        fill = bar_width * (self.enemy.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, (255, 150, 0), 
                        (WINDOW_WIDTH - 250, 120, fill, bar_height))
        
        # Pantalla de inicio
        if self.round_start:
            fight_text = self.font_large.render("FIGHT!", True, RED)
            text_rect = fight_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(fight_text, text_rect)
        
        # Pantalla de fin
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            if self.winner == "PLAYER":
                result = self.font_large.render("¡GANASTE!", True, GREEN)
            else:
                result = self.font_large.render("¡PERDISTE!", True, RED)
            
            restart = self.font_small.render("Presiona R para reiniciar", True, YELLOW)
            
            result_rect = result.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            restart_rect = restart.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
            
            self.screen.blit(result, result_rect)
            self.screen.blit(restart, restart_rect)
        
        pygame.display.flip()
        
    def run(self):
        """Loop principal"""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()