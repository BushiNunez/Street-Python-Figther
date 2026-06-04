"""Lógica principal del juego con Pygame - Versión final mejorada"""
import pygame
import random
import math
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
        
        if self.player.is_attacking and distance < PUNCH_RANGE:
            if not self.player.attack_damage_dealt:
                damage = PUNCH_DAMAGE if self.player.attack_type == 'punch' else KICK_DAMAGE
                self.enemy.take_damage(damage)
                self.player.attack_damage_dealt = True
                print(f"¡Golpe! Daño: {damage}")
            
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
        
        # Actualizar dirección
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

    def draw_detailed_snake(self, character, is_player):
        """Dibujar serpiente mejorada con animaciones detalladas"""
        x = int(character.x)
        y = int(character.y)
        facing_right = character.facing_right
        
        # Colores
        if is_player:
            main_color = (102, 221, 0)
            dark_color = (51, 153, 0)
            light_color = (153, 255, 0)
            accent = (255, 0, 0)
            belt_color = (255, 0, 0)
            skin = (200, 200, 150)
            muscle_highlight = (200, 255, 100)
        else:
            main_color = (255, 153, 0)
            dark_color = (204, 102, 0)
            light_color = (255, 200, 100)
            accent = (0, 100, 255)
            belt_color = (0, 100, 255)
            skin = (220, 180, 120)
            muscle_highlight = (255, 220, 150)
        
        # ========== ANIMACIÓN BASE ==========
        walk_cycle = self.animation_frame % 40
        
        # Movimiento de piernas (alternancia)
        left_leg_offset = math.sin(walk_cycle * math.pi / 20) * 8
        right_leg_offset = math.sin((walk_cycle + 20) * math.pi / 20) * 8
        
        # Movimiento de brazos (opuesto a piernas)
        left_arm_swing = math.sin(walk_cycle * math.pi / 20) * 10
        right_arm_swing = math.sin((walk_cycle + 20) * math.pi / 20) * 10
        
        # ========== COLA (lado opuesto) ==========
        tail_dir = -1 if facing_right else 1
        tail_x = x + (100 * tail_dir)
        
        for i in range(10):
            seg_x = tail_x + (tail_dir * i * 20)
            tail_wave = math.sin(self.animation_frame * 0.2 + i * 0.5) * 15
            seg_y = y + 50 + tail_wave
            radius = 16 - (i * 1.5)
            
            if radius > 2:
                pygame.draw.circle(self.screen, main_color, (int(seg_x), int(seg_y)), int(radius))
                pygame.draw.circle(self.screen, dark_color, (int(seg_x), int(seg_y)), int(radius), 2)
        
        # ========== PATAS ==========
        # Pata trasera izquierda (se mueve con pierna izquierda)
        pata_iz_x = x - 55
        pata_iz_y = y + 55 + left_leg_offset
        
        # Muslo
        pygame.draw.ellipse(self.screen, main_color, (pata_iz_x - 12, pata_iz_y - 15, 25, 40))
        pygame.draw.ellipse(self.screen, dark_color, (pata_iz_x - 12, pata_iz_y - 15, 25, 40), 2)
        
        # Pantorrilla
        pantorrilla_y = pata_iz_y + 25
        pygame.draw.ellipse(self.screen, main_color, (pata_iz_x - 10, pantorrilla_y, 20, 35))
        pygame.draw.ellipse(self.screen, dark_color, (pata_iz_x - 10, pantorrilla_y, 20, 35), 2)
        
        # Pie/garra
        pie_y = pantorrilla_y + 35
        pygame.draw.circle(self.screen, dark_color, (int(pata_iz_x), int(pie_y)), 10)
        pygame.draw.polygon(self.screen, dark_color, [
            (pata_iz_x - 12, pie_y),
            (pata_iz_x - 8, pie_y + 12),
            (pata_iz_x + 4, pie_y + 10),
            (pata_iz_x + 12, pie_y + 8)
        ])
        
        # Pata trasera derecha (se mueve con pierna derecha)
        pata_der_x = x + 55
        pata_der_y = y + 55 + right_leg_offset
        
        # Muslo
        pygame.draw.ellipse(self.screen, main_color, (pata_der_x - 12, pata_der_y - 15, 25, 40))
        pygame.draw.ellipse(self.screen, dark_color, (pata_der_x - 12, pata_der_y - 15, 25, 40), 2)
        
        # Pantorrilla
        pantorrilla_y = pata_der_y + 25
        pygame.draw.ellipse(self.screen, main_color, (pata_der_x - 10, pantorrilla_y, 20, 35))
        pygame.draw.ellipse(self.screen, dark_color, (pata_der_x - 10, pantorrilla_y, 20, 35), 2)
        
        # Pie/garra
        pie_y = pantorrilla_y + 35
        pygame.draw.circle(self.screen, dark_color, (int(pata_der_x), int(pie_y)), 10)
        pygame.draw.polygon(self.screen, dark_color, [
            (pata_der_x - 12, pie_y),
            (pata_der_x - 8, pie_y + 12),
            (pata_der_x + 4, pie_y + 10),
            (pata_der_x + 12, pie_y + 8)
        ])
        
        # ========== CUERPO ==========
        # Vientre claro
        pygame.draw.ellipse(self.screen, skin, (x - 38, y - 20, 76, 100))
        
        # Lado izquierdo del cuerpo
        pygame.draw.ellipse(self.screen, main_color, (x - 52, y - 25, 48, 110))
        pygame.draw.ellipse(self.screen, muscle_highlight, (x - 50, y - 15, 16, 90))
        
        # Lado derecho del cuerpo
        pygame.draw.ellipse(self.screen, main_color, (x + 4, y - 25, 48, 110))
        pygame.draw.ellipse(self.screen, muscle_highlight, (x + 34, y - 15, 16, 90))
        
        # Detalles musculares
        for i in range(4):
            y_off = y - 10 + (i * 25)
            pygame.draw.line(self.screen, dark_color, (x - 40, y_off), (x - 20, y_off), 3)
            pygame.draw.line(self.screen, dark_color, (x + 20, y_off), (x + 40, y_off), 3)
        
        # ========== CINTURÓN ==========
        pygame.draw.rect(self.screen, belt_color, (x - 48, y + 35, 96, 22))
        pygame.draw.rect(self.screen, (0, 0, 0), (x - 48, y + 35, 96, 22), 3)
        
        label = "P1" if is_player else "CPU"
        label_text = self.font_tiny.render(label, True, (255, 255, 0))
        self.screen.blit(label_text, (x - 10, y + 40))
        
        # ========== BRAZOS DETALLADOS ==========
        arm_attack_lift = 0
        arm_attack_extend = 0
        
        if character.is_attacking:
            frame_attack = character.attack_timer
            arm_attack_lift = -20 + (frame_attack * 2)
            if character.attack_type == 'punch':
                arm_attack_extend = (10 - frame_attack) * 8
            else:
                arm_attack_extend = (10 - frame_attack) * 12
        
        # BRAZO IZQUIERDO
        brazo_iz_x = x - 58
        brazo_iz_y = y - 20 + arm_attack_lift
        
        if facing_right:
            brazo_iz_swing = left_arm_swing * 0.5  # Menor movimiento en brazo trasero
            brazo_iz_x += brazo_iz_swing
        else:
            brazo_iz_swing = left_arm_swing * 1.2  # Mayor movimiento en brazo delantero
            brazo_iz_x += brazo_iz_swing
        
        # Hombro
        pygame.draw.circle(self.screen, main_color, (int(brazo_iz_x), int(brazo_iz_y)), 12)
        
        # Bíceps/muslo superior
        biceps_end_x = brazo_iz_x - 20 - arm_attack_extend
        biceps_end_y = brazo_iz_y + 15
        pygame.draw.line(self.screen, main_color, (brazo_iz_x, brazo_iz_y), 
                        (biceps_end_x, biceps_end_y), 18)
        pygame.draw.line(self.screen, muscle_highlight, (brazo_iz_x, brazo_iz_y), 
                        (biceps_end_x, biceps_end_y), 8)
        
        # Codo
        pygame.draw.circle(self.screen, dark_color, (int(biceps_end_x), int(biceps_end_y)), 10)
        
        # Antebrazo
        antebrazo_end_x = biceps_end_x - 20 - arm_attack_extend
        antebrazo_end_y = biceps_end_y + 20
        pygame.draw.line(self.screen, main_color, (biceps_end_x, biceps_end_y), 
                        (antebrazo_end_x, antebrazo_end_y), 15)
        
        # Puño grande
        pygame.draw.circle(self.screen, dark_color, (int(antebrazo_end_x), int(antebrazo_end_y)), 14)
        pygame.draw.circle(self.screen, (150, 150, 150), (int(antebrazo_end_x), int(antebrazo_end_y)), 10)
        
        # BRAZO DERECHO
        brazo_der_x = x + 58
        brazo_der_y = y - 20 + arm_attack_lift
        
        if facing_right:
            brazo_der_swing = right_arm_swing * 1.2  # Mayor movimiento en brazo delantero
            brazo_der_x += brazo_der_swing
        else:
            brazo_der_swing = right_arm_swing * 0.5  # Menor movimiento en brazo trasero
            brazo_der_x += brazo_der_swing
        
        # Hombro
        pygame.draw.circle(self.screen, main_color, (int(brazo_der_x), int(brazo_der_y)), 12)
        
        # Bíceps
        biceps_end_x = brazo_der_x + 20 + arm_attack_extend
        biceps_end_y = brazo_der_y + 15
        pygame.draw.line(self.screen, main_color, (brazo_der_x, brazo_der_y), 
                        (biceps_end_x, biceps_end_y), 18)
        pygame.draw.line(self.screen, muscle_highlight, (brazo_der_x, brazo_der_y), 
                        (biceps_end_x, biceps_end_y), 8)
        
        # Codo
        pygame.draw.circle(self.screen, dark_color, (int(biceps_end_x), int(biceps_end_y)), 10)
        
        # Antebrazo
        antebrazo_end_x = biceps_end_x + 20 + arm_attack_extend
        antebrazo_end_y = biceps_end_y + 20
        pygame.draw.line(self.screen, main_color, (biceps_end_x, biceps_end_y), 
                        (antebrazo_end_x, antebrazo_end_y), 15)
        
        # Puño grande
        pygame.draw.circle(self.screen, dark_color, (int(antebrazo_end_x), int(antebrazo_end_y)), 14)
        pygame.draw.circle(self.screen, (150, 150, 150), (int(antebrazo_end_x), int(antebrazo_end_y)), 10)
        
        # ========== CUELLO ==========
        pygame.draw.ellipse(self.screen, main_color, (x - 28, y - 90, 56, 35))
        pygame.draw.ellipse(self.screen, dark_color, (x - 28, y - 90, 56, 35), 2)
        
        # ========== CABEZA ==========
        head_x = x
        head_y = y - 115
        
        # Cráneo
        pygame.draw.ellipse(self.screen, main_color, (head_x - 48, head_y - 30, 96, 70))
        pygame.draw.ellipse(self.screen, dark_color, (head_x - 48, head_y - 30, 96, 70), 3)
        
        # Mandíbula
        pygame.draw.polygon(self.screen, main_color, [
            (head_x - 38, head_y + 30),
            (head_x + 38, head_y + 30),
            (head_x + 42, head_y + 45),
            (head_x - 42, head_y + 45)
        ])
        
        # Paladar/boca
        pygame.draw.polygon(self.screen, skin, [
            (head_x - 28, head_y + 18),
            (head_x + 28, head_y + 18),
            (head_x + 24, head_y + 35),
            (head_x - 24, head_y + 35)
        ])
        
        # Colmillos superiores
        pygame.draw.polygon(self.screen, (255, 255, 255), [
            (head_x - 16, head_y + 18),
            (head_x - 20, head_y + 40),
            (head_x - 12, head_y + 28)
        ])
        
        pygame.draw.polygon(self.screen, (255, 255, 255), [
            (head_x + 16, head_y + 18),
            (head_x + 20, head_y + 40),
            (head_x + 12, head_y + 28)
        ])
        
        # Escamas faciales
        pygame.draw.line(self.screen, dark_color, (head_x - 40, head_y - 5), (head_x - 15, head_y + 5), 3)
        pygame.draw.line(self.screen, dark_color, (head_x + 40, head_y - 5), (head_x + 15, head_y + 5), 3)
        pygame.draw.line(self.screen, dark_color, (head_x - 45, head_y + 10), (head_x - 20, head_y + 15), 2)
        pygame.draw.line(self.screen, dark_color, (head_x + 45, head_y + 10), (head_x + 20, head_y + 15), 2)
        
        # OJOS
        if facing_right:
            eye_left_x = head_x - 18
            eye_right_x = head_x + 18
        else:
            eye_left_x = head_x - 18
            eye_right_x = head_x + 18
        
        eye_y = head_y - 15
        
        # Ojo izquierdo
        pygame.draw.ellipse(self.screen, (255, 255, 0), (eye_left_x - 14, eye_y - 10, 28, 20))
        pygame.draw.ellipse(self.screen, (0, 0, 0), (eye_left_x - 10, eye_y - 6, 14, 12))
        pygame.draw.circle(self.screen, (255, 255, 0), (eye_left_x - 5, eye_y - 2), 4)
        
        # Ojo derecho
        pygame.draw.ellipse(self.screen, (255, 255, 0), (eye_right_x - 14, eye_y - 10, 28, 20))
        pygame.draw.ellipse(self.screen, (0, 0, 0), (eye_right_x - 10, eye_y - 6, 14, 12))
        pygame.draw.circle(self.screen, (255, 255, 0), (eye_right_x - 5, eye_y - 2), 4)
        
        # Nariz
        pygame.draw.polygon(self.screen, dark_color, [
            (head_x, head_y),
            (head_x - 6, head_y + 8),
            (head_x + 6, head_y + 8)
        ])
        
        # ========== CRESTA ROJA ==========
        crest_y = head_y - 32
        for i in range(5):
            crest_x = head_x - 30 + (i * 15)
            pygame.draw.polygon(self.screen, accent, [
                (crest_x, crest_y),
                (crest_x - 9, crest_y - 22),
                (crest_x + 9, crest_y - 22)
            ])
            pygame.draw.line(self.screen, (0, 0, 0), 
                            (crest_x - 9, crest_y - 22),
                            (crest_x + 9, crest_y - 22), 2)
        
        # ========== LENGUA ANIMADA ==========
        if character.is_attacking:
            tongue_length = 40 + (self.animation_frame % 15) * 3
            tongue_y = head_y + 40
            
            tongue_dir = 1 if facing_right else -1
            
            pygame.draw.polygon(self.screen, accent, [
                (head_x + (45 * tongue_dir), tongue_y - 10),
                (head_x + ((45 + tongue_length) * tongue_dir), tongue_y - 15),
                (head_x + ((45 + tongue_length) * tongue_dir), tongue_y + 15),
                (head_x + (45 * tongue_dir), tongue_y + 10)
            ])
        
        # ========== AURA ==========
        if character.attack_timer > 5:
            aura_radius = 130 + (self.animation_frame % 10) * 2
            pygame.draw.circle(self.screen, (255, 255, 0), (head_x, head_y - 30), aura_radius, 4)
            
            for i in range(12):
                angle = (i * 30 + self.animation_frame * 8) * math.pi / 180
                length = 140 + (self.animation_frame % 5) * 5
                end_x = head_x + length * math.cos(angle)
                end_y = head_y - 30 + length * math.sin(angle)
                pygame.draw.line(self.screen, (255, 255, 0), 
                               (head_x, head_y - 30), 
                               (int(end_x), int(end_y)), 2)
            
    def draw(self):
        """Dibujar pantalla"""
        self.screen.fill(DARK_BG)
        
        # Fondo con edificios
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
        self.draw_detailed_snake(self.player, True)
        self.draw_detailed_snake(self.enemy, False)
        
        # UI - Nombres
        player_name = self.font_medium.render("SNAKE-KYU", True, GREEN)
        self.screen.blit(player_name, (20, 15))
        
        enemy_name = self.font_medium.render("RATTLER", True, (255, 150, 0))
        enemy_name_rect = enemy_name.get_rect()
        self.screen.blit(enemy_name, (WINDOW_WIDTH - enemy_name_rect.width - 20, 15))
        
        # Round
        round_text = self.font_large.render(f"ROUND {self.round_number}", True, RED)
        round_rect = round_text.get_rect(center=(WINDOW_WIDTH // 2, 35))
        self.screen.blit(round_text, round_rect)
        
        # HP Bars
        bar_width = 280
        bar_height = 28
        
        # Player
        pygame.draw.rect(self.screen, RED, (15, 90, bar_width, bar_height))
        fill = bar_width * (self.player.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, GREEN, (15, 90, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (15, 90, bar_width, bar_height), 3)
        
        player_hp_text = self.font_small.render(f"{int(self.player.health)}/{HEALTH_MAX}", True, WHITE)
        self.screen.blit(player_hp_text, (30, 95))
        
        # Enemy
        pygame.draw.rect(self.screen, RED, (WINDOW_WIDTH - 15 - bar_width, 90, bar_width, bar_height))
        fill = bar_width * (self.enemy.health / HEALTH_MAX)
        pygame.draw.rect(self.screen, (255, 150, 0), 
                        (WINDOW_WIDTH - 15 - bar_width + (bar_width - fill), 90, fill, bar_height))
        pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - 15 - bar_width, 90, bar_width, bar_height), 3)
        
        enemy_hp_text = self.font_small.render(f"{int(self.enemy.health)}/{HEALTH_MAX}", True, WHITE)
        enemy_hp_rect = enemy_hp_text.get_rect()
        self.screen.blit(enemy_hp_text, (WINDOW_WIDTH - 30 - enemy_hp_rect.width, 95))
        
        # Pantalla inicio
        if self.round_start:
            fight_text = self.font_title.render("FIGHT!", True, RED)
            text_rect = fight_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            # Efecto de pulso
            pulse = 1 + math.sin(self.round_start_timer * 0.1) * 0.1
            scaled_rect = text_rect.copy()
            self.screen.blit(fight_text, text_rect)
        
        # Pantalla fin
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
        
    def run(self):
        """Loop principal"""
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()