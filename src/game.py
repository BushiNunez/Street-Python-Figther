"""Lógica principal del juego con Pygame - Versión mejorada"""
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
        self.round_start_timer = 120  # 2 segundos a 60 FPS
        self.round_number = 1
        
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
        
        if not self.round_start and not self.game_over:
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

    def draw_detailed_snake(self, character, is_player):
        """Dibujar serpiente muy detallada tipo Street Fighter"""
        x = int(character.x)
        y = int(character.y)
        
        # Colores según personaje
        if is_player:
            # Verde con detalles
            main_color = (102, 221, 0)      # Verde brillante
            dark_color = (51, 153, 0)       # Verde oscuro
            light_color = (153, 255, 0)     # Verde claro
            accent = (255, 0, 0)            # Rojo
            belt_color = (255, 0, 0)        # Rojo
            skin = (200, 200, 150)          # Beige para vientre
        else:
            # Naranja con detalles
            main_color = (255, 153, 0)      # Naranja
            dark_color = (204, 102, 0)      # Naranja oscuro
            light_color = (255, 200, 100)   # Naranja claro
            accent = (0, 100, 255)          # Azul
            belt_color = (0, 100, 255)      # Azul
            skin = (220, 180, 120)          # Beige oscuro
        
        # ========== COLA ==========
        tail_start_x = x - 80
        tail_start_y = y + 50
        
        for i in range(8):
            seg_x = tail_start_x - (i * 25)
            seg_y = tail_start_y + (8 * ((i % 2) * 2 - 1))
            radius = 18 - (i * 2)
            
            pygame.draw.circle(self.screen, main_color, (seg_x, seg_y), radius)
            pygame.draw.circle(self.screen, dark_color, (seg_x, seg_y), radius, 2)
            
            pygame.draw.arc(self.screen, dark_color, 
                           (seg_x - radius, seg_y - radius, radius * 2, radius * 2),
                           0, 3.14, 2)
        
        # ========== PATAS ==========
        # Pata trasera izquierda
        pygame.draw.ellipse(self.screen, main_color, (x - 60, y + 50, 25, 35))
        pygame.draw.circle(self.screen, dark_color, (x - 47, y + 85), 10)
        pygame.draw.polygon(self.screen, dark_color, [
            (x - 52, y + 85),
            (x - 47, y + 95),
            (x - 42, y + 85)
        ])
        
        # Pata trasera derecha
        pygame.draw.ellipse(self.screen, main_color, (x + 35, y + 50, 25, 35))
        pygame.draw.circle(self.screen, dark_color, (x + 47, y + 85), 10)
        pygame.draw.polygon(self.screen, dark_color, [
            (x + 42, y + 85),
            (x + 47, y + 95),
            (x + 52, y + 85)
        ])
        
        # ========== CUERPO PRINCIPAL ==========
        # Vientre
        pygame.draw.ellipse(self.screen, skin, (x - 35, y - 25, 70, 110))
        
        # Cuerpo musculoso izquierdo
        pygame.draw.ellipse(self.screen, main_color, (x - 50, y - 30, 50, 120))
        
        # Cuerpo musculoso derecho
        pygame.draw.ellipse(self.screen, main_color, (x, y - 30, 50, 120))
        
        # Detalles musculares
        for i in range(3):
            y_offset = y - 20 + (i * 35)
            pygame.draw.line(self.screen, dark_color, (x - 40, y_offset), (x - 20, y_offset), 2)
            pygame.draw.line(self.screen, dark_color, (x + 20, y_offset), (x + 40, y_offset), 2)
        
        # ========== CINTURÓN ==========
        pygame.draw.rect(self.screen, belt_color, (x - 45, y + 35, 90, 20))
        pygame.draw.rect(self.screen, (0, 0, 0), (x - 45, y + 35, 90, 20), 2)
        
        label = "P1" if is_player else "CPU"
        label_text = self.font_tiny.render(label, True, (255, 255, 0))
        self.screen.blit(label_text, (x - 8, y + 40))
        
        # ========== BRAZOS ==========
        arm_lift = 0
        if character.is_attacking:
            arm_lift = -15 + (self.animation_frame % 10) * 3
        
        # Brazo izquierdo
        arm_left_x = x - 55
        arm_left_y = y - 15 + arm_lift
        
        pygame.draw.ellipse(self.screen, main_color, (arm_left_x - 25, arm_left_y - 20, 40, 50))
        pygame.draw.circle(self.screen, dark_color, (arm_left_x - 10, arm_left_y), 8)
        pygame.draw.ellipse(self.screen, main_color, (arm_left_x - 40, arm_left_y + 20, 25, 45))
        pygame.draw.ellipse(self.screen, dark_color, (arm_left_x - 50, arm_left_y + 45, 35, 40))
        pygame.draw.circle(self.screen, (150, 150, 150), (arm_left_x - 35, arm_left_y + 65), 12)
        pygame.draw.line(self.screen, (100, 100, 100), 
                        (arm_left_x - 48, arm_left_y + 55),
                        (arm_left_x - 22, arm_left_y + 55), 3)
        
        # Brazo derecho
        arm_right_x = x + 55
        arm_right_y = y - 15 + arm_lift
        
        pygame.draw.ellipse(self.screen, main_color, (arm_right_x - 15, arm_right_y - 20, 40, 50))
        pygame.draw.circle(self.screen, dark_color, (arm_right_x + 10, arm_right_y), 8)
        pygame.draw.ellipse(self.screen, main_color, (arm_right_x + 15, arm_right_y + 20, 25, 45))
        pygame.draw.ellipse(self.screen, dark_color, (arm_right_x + 15, arm_right_y + 45, 35, 40))
        pygame.draw.circle(self.screen, (150, 150, 150), (arm_right_x + 35, arm_right_y + 65), 12)
        pygame.draw.line(self.screen, (100, 100, 100), 
                        (arm_right_x + 22, arm_right_y + 55),
                        (arm_right_x + 48, arm_right_y + 55), 3)
        
        # ========== CUELLO ==========
        pygame.draw.ellipse(self.screen, main_color, (x - 25, y - 85, 50, 30))
        
        # ========== CABEZA ==========
        head_x = x
        head_y = y - 110
        
        # Forma base
        pygame.draw.ellipse(self.screen, main_color, (head_x - 45, head_y - 35, 90, 75))
        
        # Mandíbula
        pygame.draw.polygon(self.screen, main_color, [
            (head_x - 35, head_y + 25),
            (head_x + 35, head_y + 25),
            (head_x + 40, head_y + 40),
            (head_x - 40, head_y + 40)
        ])
        
        # Paladar
        pygame.draw.polygon(self.screen, skin, [
            (head_x - 25, head_y + 15),
            (head_x + 25, head_y + 15),
            (head_x + 20, head_y + 30),
            (head_x - 20, head_y + 30)
        ])
        
        # Colmillos
        pygame.draw.polygon(self.screen, (255, 255, 255), [
            (head_x - 15, head_y + 15),
            (head_x - 18, head_y + 35),
            (head_x - 12, head_y + 25)
        ])
        
        pygame.draw.polygon(self.screen, (255, 255, 255), [
            (head_x + 15, head_y + 15),
            (head_x + 18, head_y + 35),
            (head_x + 12, head_y + 25)
        ])
        
        # Escamas faciales
        pygame.draw.line(self.screen, dark_color, (head_x - 35, head_y - 10), (head_x - 15, head_y), 2)
        pygame.draw.line(self.screen, dark_color, (head_x + 35, head_y - 10), (head_x + 15, head_y), 2)
        
        # Ojos
        eye_left_x = head_x - 15
        eye_left_y = head_y - 15
        pygame.draw.ellipse(self.screen, (255, 255, 0), (eye_left_x - 12, eye_left_y - 8, 24, 16))
        pygame.draw.ellipse(self.screen, (0, 0, 0), (eye_left_x - 8, eye_left_y - 4, 12, 8))
        pygame.draw.circle(self.screen, (255, 255, 0), (eye_left_x - 3, eye_left_y - 2), 3)
        
        eye_right_x = head_x + 15
        eye_right_y = head_y - 15
        pygame.draw.ellipse(self.screen, (255, 255, 0), (eye_right_x - 12, eye_right_y - 8, 24, 16))
        pygame.draw.ellipse(self.screen, (0, 0, 0), (eye_right_x - 8, eye_right_y - 4, 12, 8))
        pygame.draw.circle(self.screen, (255, 255, 0), (eye_right_x - 3, eye_right_y - 2), 3)
        
        # Nariz
        pygame.draw.polygon(self.screen, dark_color, [
            (head_x, head_y - 5),
            (head_x - 5, head_y + 5),
            (head_x + 5, head_y + 5)
        ])
        
        # ========== CRESTA ==========
        crest_y = head_y - 35
        for i in range(4):
            crest_x = head_x - 25 + (i * 17)
            pygame.draw.polygon(self.screen, accent, [
                (crest_x, crest_y),
                (crest_x - 8, crest_y - 20),
                (crest_x + 8, crest_y - 20)
            ])
            pygame.draw.line(self.screen, (0, 0, 0), 
                            (crest_x - 8, crest_y - 20),
                            (crest_x + 8, crest_y - 20), 1)
        
        # ========== LENGUA ==========
        if character.is_attacking:
            tongue_length = 35 + (self.animation_frame % 15) * 2
            tongue_y = head_y + 35
            
            if character.facing_right:
                points = [
                    (head_x + 40, tongue_y - 8),
                    (head_x + 40 + tongue_length, tongue_y - 12),
                    (head_x + 40 + tongue_length, tongue_y + 12),
                    (head_x + 40, tongue_y + 8)
                ]
            else:
                points = [
                    (head_x - 40, tongue_y - 8),
                    (head_x - 40 - tongue_length, tongue_y - 12),
                    (head_x - 40 - tongue_length, tongue_y + 12),
                    (head_x - 40, tongue_y + 8)
                ]
            
            pygame.draw.polygon(self.screen, accent, points)
            pygame.draw.polygon(self.screen, (150, 0, 0), points, 2)
        
        # ========== AURA ==========
        if character.attack_timer > 5:
            aura_radius = 120 + (self.animation_frame % 10) * 2
            pygame.draw.circle(self.screen, (255, 255, 0), (head_x, head_y - 30), aura_radius, 3)
            
            for i in range(8):
                angle = (i * 45 + self.animation_frame * 5) * 3.14159 / 180
                length = 130 + (self.animation_frame % 5) * 5
                end_x = head_x + length * __import__('math').cos(angle)
                end_y = head_y - 30 + length * __import__('math').sin(angle)
                pygame.draw.line(self.screen, (255, 255, 0), 
                               (head_x, head_y - 30), 
                               (int(end_x), int(end_y)), 1)
            
    def draw(self):
        """Dibujar pantalla"""
        self.screen.fill(DARK_BG)
        
        # Fondo con "edificios"
        for i in range(0, WINDOW_WIDTH, 100):
            pygame.draw.rect(self.screen, (40, 40, 60), (i, 0, 80, 100))
            pygame.draw.line(self.screen, (100, 100, 150), (i, 0), (i, 100), 1)
        
        # Línea divisoria
        pygame.draw.line(self.screen, RED, 
                        (WINDOW_WIDTH // 2, 150), 
                        (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50), 2)
        
        # Personajes
        self.draw_detailed_snake(self.player, True)
        self.draw_detailed_snake(self.enemy, False)
        
        # UI - Top left (Jugador)
        player_name = self.font_medium.render("SNAKE-KYU", True, GREEN)
        self.screen.blit(player_name, (20, 20))
        
        # UI - Top right (Enemigo)
        enemy_name = self.font_medium.render("RATTLER", True, (255, 150, 0))
        enemy_name_rect = enemy_name.get_rect()
        self.screen.blit(enemy_name, (WINDOW_WIDTH - enemy_name_rect.width - 20, 20))
        
        # Round
        round_text = self.font_large.render(f"ROUND {self.round_number}", True, RED)
        round_rect = round_text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(round_text, round_rect)
        
        # Barras de salud
        bar_width = 250
        bar_height = 25
        
        # Player HP bar
        pygame.draw.rect(self.screen, RED, (20, 70, bar_width, bar_height))
        fill = bar_width * (self.player.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, GREEN, (20, 70, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (20, 70, bar_width, bar_height), 2)
        
        player_hp_text = self.font_small.render(f"{int(self.player.health)}", True, WHITE)
        self.screen.blit(player_hp_text, (30, 72))
        
        # Enemy HP bar
        pygame.draw.rect(self.screen, RED, (WINDOW_WIDTH - 20 - bar_width, 70, bar_width, bar_height))
        fill = bar_width * (self.enemy.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, (255, 150, 0), 
                        (WINDOW_WIDTH - 20 - bar_width + (bar_width - fill), 70, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - 20 - bar_width, 70, bar_width, bar_height), 2)
        
        enemy_hp_text = self.font_small.render(f"{int(self.enemy.health)}", True, WHITE)
        enemy_hp_rect = enemy_hp_text.get_rect()
        self.screen.blit(enemy_hp_text, (WINDOW_WIDTH - 30 - enemy_hp_rect.width, 72))
        
        # Pantalla de inicio
        if self.round_start:
            fight_text = self.font_title.render("FIGHT!", True, RED)
            text_rect = fight_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            # Efecto de pulsación
            scale = 1 + (self.round_start_timer % 30) * 0.02
            shadow = pygame.Surface(fight_text.get_size())
            shadow.fill(DARK_BG)
            self.screen.blit(fight_text, text_rect)
        
        # Pantalla de fin
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(180)
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
        
    def run(self):
        """Loop principal"""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()