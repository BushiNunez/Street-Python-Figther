"""Lógica principal del juego"""
import tkinter as tk
import random
from src.constants import *
from src.character import Character
from src.enemy import Enemy

class Game:
    """Clase principal que controla la lógica del juego"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
        # Canvas para dibujar
        self.canvas = tk.Canvas(
            root, 
            width=WINDOW_WIDTH, 
            height=WINDOW_HEIGHT, 
            bg='#1a1a2e'  # Fondo oscuro tipo arcade
        )
        self.canvas.pack()
        
        # Personajes
        self.player = Character(PLAYER_X, CHARACTER_Y, color='#00ff41', is_player=True)
        self.enemy = Enemy(ENEMY_X, CHARACTER_Y)
        self.enemy.color = '#ff6b35'  # Color naranja para el enemigo
        
        # Estado del juego
        self.running = True
        self.game_over = False
        self.winner = None
        self.animation_frame = 0  # ← NUEVO: Contador de animación
        
        # Controles
        self.keys = {}
        self.root.bind('<KeyPress>', self._key_press)
        self.root.bind('<KeyRelease>', self._key_release)
        
        # Iniciar loop del juego
        self._game_loop()
        
    def _key_press(self, event):
        """Manejar tecla presionada"""
        self.keys[event.char.lower()] = True
        self.keys[event.keysym.lower()] = True
        
    def _key_release(self, event):
        """Manejar tecla soltada"""
        self.keys[event.char.lower()] = False
        self.keys[event.keysym.lower()] = False
        
    def _handle_input(self):
        """Procesar entrada del jugador"""
        # Movimiento
        if self.keys.get('left', False) or self.keys.get('a', False):
            self.player.move_left()
        if self.keys.get('right', False) or self.keys.get('d', False):
            self.player.move_right()
            
        # Ataques
        if self.keys.get('z', False):
            self.player.punch()
        if self.keys.get('x', False):
            self.player.kick()
            
    def _check_collisions(self):
        """Verificar si los ataques conectan"""
        distance = abs(self.player.x - self.enemy.x)
        
        # Ataque del jugador
        if self.player.is_attacking and distance < PUNCH_RANGE:
            if not self.player.attack_damage_dealt:
                damage = (PUNCH_DAMAGE if self.player.attack_type == 'punch' 
                         else KICK_DAMAGE)
                self.enemy.take_damage(damage)
                self.player.attack_damage_dealt = True
                print(f"¡Golpe! Daño al enemigo: {damage}")
            
        # Ataque del enemigo
        if self.enemy.is_attacking and distance < PUNCH_RANGE:
            if not self.enemy.attack_damage_dealt:
                damage = (PUNCH_DAMAGE if self.enemy.attack_type == 'punch' 
                         else KICK_DAMAGE)
                self.player.take_damage(damage)
                self.enemy.attack_damage_dealt = True
                print(f"¡Golpe del enemigo! Daño al jugador: {damage}")
            
    def _update(self):
        """Actualizar lógica del juego"""
        if self.game_over:
            return
            
        self._handle_input()
        self.player.update()
        self.enemy.update(self.player)
        self._check_collisions()
        self.animation_frame += 1  # ← NUEVO: Incrementar animación
        
        # Verificar condición de victoria
        if not self.player.is_alive():
            self.game_over = True
            self.winner = "ENEMY"
        elif not self.enemy.is_alive():
            self.game_over = True
            self.winner = "PLAYER"
            
    def _draw(self):
        """Dibujar elementos del juego"""
        self.canvas.delete('all')
        
        # Fondo con gradiente (simulado)
        self.canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill='#0a0e27')
        
        # Línea separadora del ring
        self.canvas.create_line(
            WINDOW_WIDTH // 2, 100, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100,
            fill='#ff6b35', width=2, dash=(10, 10)
        )
        
        # Personajes (serpientes mejoradas)
        self._draw_snake(self.player, is_player=True)
        self._draw_snake(self.enemy, is_player=False)
        
        # Barras de salud
        self._draw_health_bar(self.player, 20, 20, '#00ff41')
        self._draw_health_bar(self.enemy, WINDOW_WIDTH - 220, 20, '#ff6b35')
        
        # Controles
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30,
            text="[A/D o ←→] Mover | [Z] Puñetazo | [X] Patada",
            fill='#00ff41', font=('Courier', 10, 'bold')
        )
        
        # Pantalla de fin de juego
        if self.game_over:
            self._draw_game_over()
            
    def _draw_snake(self, character, is_player=True):
        """Dibujar serpiente musculosa tipo Street Fighter"""
        head_x = character.x
        head_y = character.y
        
        # Colores
        if is_player:
            main_color = '#66dd00'      # Verde fluorescente
            dark_color = '#339900'      # Verde oscuro
            accent_color = '#ffff00'    # Amarillo
            belt_color = '#dd0000'      # Rojo
        else:
            main_color = '#ff9900'      # Naranja
            dark_color = '#cc6600'      # Naranja oscuro
            accent_color = '#ffff00'    # Amarillo
            belt_color = '#0066ff'      # Azul
        
        # ========== COLA ==========
        tail_segments = 8
        tail_x = head_x - 150
        for i in range(tail_segments):
            segment_x = head_x - 100 - (i * 20)
            segment_y = head_y + 40 + (10 * ((i % 2) - 0.5))
            size = 15 - i
            
            # Segmento de cola
            self.canvas.create_oval(
                segment_x - size, segment_y - size,
                segment_x + size, segment_y + size,
                fill=main_color, outline=dark_color, width=2
            )
            # Escamas
            self.canvas.create_arc(
                segment_x - size, segment_y - size,
                segment_x + size, segment_y + size,
                start=0, extent=180, outline=dark_color, width=1
            )
        
        # ========== CUERPO PRINCIPAL ==========
        body_width = 70
        body_height = 80
        
        # Vientre más claro
        self.canvas.create_oval(
            head_x - body_width + 10, head_y - body_height // 2,
            head_x + body_width - 10, head_y + body_height // 2,
            fill='#99ff00', outline=dark_color, width=2
        )
        
        # Músculos del cuerpo (sombreado)
        self.canvas.create_arc(
            head_x - body_width, head_y - body_height // 2,
            head_x - body_width + 40, head_y + body_height // 2,
            start=90, extent=180, fill=dark_color, outline=dark_color
        )
        
        self.canvas.create_arc(
            head_x + body_width - 40, head_y - body_height // 2,
            head_x + body_width, head_y + body_height // 2,
            start=270, extent=180, fill=dark_color, outline=dark_color
        )
        
        # ========== CINTURÓN ROJO ==========
        self.canvas.create_rectangle(
            head_x - body_width - 5, head_y + body_height // 2 - 15,
            head_x + body_width + 5, head_y + body_height // 2 + 15,
            fill=belt_color, outline='#000000', width=2
        )
        
        # Símbolo en el cinturón
        self.canvas.create_text(
            head_x, head_y + body_height // 2,
            text='P1' if is_player else 'CPU',
            fill='#ffff00', font=('Arial', 12, 'bold')
        )
        
        # ========== PATAS ==========
        leg_y = head_y + body_height // 2 + 30
        
        # Pata izquierda
        self.canvas.create_oval(
            head_x - body_width + 10, leg_y - 15,
            head_x - body_width + 35, leg_y + 15,
            fill=main_color, outline=dark_color, width=2
        )
        self.canvas.create_polygon(
            head_x - body_width + 20, leg_y + 15,
            head_x - body_width + 10, leg_y + 30,
            head_x - body_width + 30, leg_y + 30,
            fill=dark_color, outline='#000000', width=1
        )
        
        # Pata derecha
        self.canvas.create_oval(
            head_x + body_width - 35, leg_y - 15,
            head_x + body_width - 10, leg_y + 15,
            fill=main_color, outline=dark_color, width=2
        )
        self.canvas.create_polygon(
            head_x + body_width - 20, leg_y + 15,
            head_x + body_width - 30, leg_y + 30,
            head_x + body_width - 10, leg_y + 30,
            fill=dark_color, outline='#000000', width=1
        )
        
        # ========== BRAZOS ==========
        arm_lift = 0 if not character.is_attacking else (-20 + (self.animation_frame % 10))
        
        # Brazo izquierdo
        arm_left_x = head_x - body_width - 20
        arm_left_y = head_y - 20 + arm_lift
        
        # Músculo del brazo
        self.canvas.create_oval(
            arm_left_x - 30, arm_left_y - 20,
            arm_left_x, arm_left_y + 20,
            fill=main_color, outline=dark_color, width=2
        )
        
        # Puño
        self.canvas.create_oval(
            arm_left_x - 50, arm_left_y - 20,
            arm_left_x - 20, arm_left_y + 20,
            fill=dark_color, outline='#000000', width=2
        )
        
        # Guante/marca del puño
        self.canvas.create_rectangle(
            arm_left_x - 45, arm_left_y - 15,
            arm_left_x - 25, arm_left_y + 15,
            fill='#666666', outline='#000000', width=1
        )
        
        # Brazo derecho
        arm_right_x = head_x + body_width + 20
        arm_right_y = head_y - 20 + arm_lift
        
        # Músculo del brazo
        self.canvas.create_oval(
            arm_right_x, arm_right_y - 20,
            arm_right_x + 30, arm_right_y + 20,
            fill=main_color, outline=dark_color, width=2
        )
        
        # Puño
        self.canvas.create_oval(
            arm_right_x + 20, arm_right_y - 20,
            arm_right_x + 50, arm_right_y + 20,
            fill=dark_color, outline='#000000', width=2
        )
        
        # Guante/marca del puño
        self.canvas.create_rectangle(
            arm_right_x + 25, arm_right_y - 15,
            arm_right_x + 45, arm_right_y + 15,
            fill='#666666', outline='#000000', width=1
        )
        
        # ========== CABEZA ==========
        head_size = 45
        
        # Cabeza principal
        self.canvas.create_oval(
            head_x - head_size, head_y - head_size - 20,
            head_x + head_size, head_y + head_size - 20,
            fill=main_color, outline=dark_color, width=3
        )
        
        # Escamas en la cabeza
        for i in range(3):
            scale_y = head_y - head_size + (i * 30)
            self.canvas.create_arc(
                head_x - head_size + 10, scale_y - 10,
                head_x - head_size + 40, scale_y + 10,
                start=0, extent=180, outline=dark_color, width=1
            )
        
        # Mandíbula/Boca
        self.canvas.create_arc(
            head_x - head_size + 5, head_y + 10,
            head_x + head_size - 5, head_y + head_size,
            start=0, extent=180, outline='#000000', width=2, fill='#ffcc00'
        )
        
        # Colmillos
        self.canvas.create_polygon(
            head_x - 10, head_y + head_size - 10,
            head_x - 15, head_y + head_size + 10,
            head_x - 5, head_y + head_size + 5,
            fill='#ffffff', outline='#000000', width=1
        )
        
        self.canvas.create_polygon(
            head_x + 10, head_y + head_size - 10,
            head_x + 5, head_y + head_size + 5,
            head_x + 15, head_y + head_size + 10,
            fill='#ffffff', outline='#000000', width=1
        )
        
        # Ojos
        eye_offset = 20
        self.canvas.create_oval(
            head_x - eye_offset - 8, head_y - 30,
            head_x - eye_offset + 8, head_y - 14,
            fill='#ffff00', outline='#000000', width=2
        )
        
        self.canvas.create_oval(
            head_x + eye_offset - 8, head_y - 30,
            head_x + eye_offset + 8, head_y - 14,
            fill='#ffff00', outline='#000000', width=2
        )
        
        # Pupila
        self.canvas.create_oval(
            head_x - eye_offset - 4, head_y - 26,
            head_x - eye_offset + 4, head_y - 18,
            fill='#000000'
        )
        
        self.canvas.create_oval(
            head_x + eye_offset - 4, head_y - 26,
            head_x + eye_offset + 4, head_y - 18,
            fill='#000000'
        )
        
        # ========== CRESTA ROJA ==========
        crest_y = head_y - head_size - 30
        for i in range(3):
            crest_x = head_x - 20 + (i * 20)
            self.canvas.create_polygon(
                crest_x, crest_y,
                crest_x - 10, crest_y - 25,
                crest_x + 10, crest_y - 25,
                fill=belt_color, outline='#000000', width=1
            )
        
        # ========== LENGUA ROJA ==========
        if character.is_attacking:
            tongue_length = 30 + (self.animation_frame % 15)
            tongue_y = head_y + head_size
            
            if character.facing_right:
                # Lengua hacia la derecha
                self.canvas.create_polygon(
                    head_x + head_size, tongue_y - 5,
                    head_x + head_size + tongue_length, tongue_y - 10,
                    head_x + head_size + tongue_length, tongue_y + 10,
                    head_x + head_size, tongue_y + 5,
                    fill=belt_color, outline='#990000', width=2
                )
            else:
                # Lengua hacia la izquierda
                self.canvas.create_polygon(
                    head_x - head_size, tongue_y - 5,
                    head_x - head_size - tongue_length, tongue_y - 10,
                    head_x - head_size - tongue_length, tongue_y + 10,
                    head_x - head_size, tongue_y + 5,
                    fill=belt_color, outline='#990000', width=2
                )
        
        # ========== AURA DE ATAQUE ==========
        if character.attack_timer > 5:
            aura_size = head_size + 60
            self.canvas.create_oval(
                head_x - aura_size, head_y - aura_size,
                head_x + aura_size, head_y + aura_size,
                outline=accent_color, width=3
            )
            
            # Líneas de energía
            for i in range(3):
                offset = (self.animation_frame % 20) * 2
                self.canvas.create_arc(
                    head_x - aura_size - offset, head_y - aura_size - offset,
                    head_x + aura_size + offset, head_y + aura_size + offset,
                    start=0, extent=90, outline=accent_color, width=1
                )
            
    def _draw_health_bar(self, character, x, y, color):
        """Dibujar barra de salud con estilo arcade"""
        bar_width = 200
        bar_height = 30
        health_percent = max(0, character.health / HEALTH_MAX)
        
        # Fondo rojo
        self.canvas.create_rectangle(x, y, x + bar_width, y + bar_height, 
                                     fill='#330000', outline=color, width=2)
        
        # Barra verde
        bar_color = '#00ff41' if health_percent > 0.3 else '#ff6b35'
        self.canvas.create_rectangle(
            x + 2, y + 2, x + 2 + ((bar_width - 4) * health_percent), y + bar_height - 2,
            fill=bar_color, outline=None
        )
        
        # Borde
        self.canvas.create_rectangle(
            x, y, x + bar_width, y + bar_height,
            fill=None, outline=color, width=2
        )
        
        # Texto
        self.canvas.create_text(
            x + bar_width // 2, y + bar_height // 2,
            text=f'HP: {int(character.health)}/{HEALTH_MAX}',
            fill='#ffff00', font=('Courier', 10, 'bold')
        )
        
    def _draw_game_over(self):
        """Mostrar pantalla de fin de juego"""
        # Fondo oscuro semi-transparente
        self.canvas.create_rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
            fill='#000000'
        )
        
        if self.winner == "PLAYER":
            text = "¡GANASTE!"
            color = '#00ff41'
        else:
            text = "¡PERDISTE!"
            color = '#ff6b35'
            
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50,
            text=text, fill=color, font=('Courier', 60, 'bold')
        )
        
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
            text="Presiona R para reiniciar",
            fill='#00ff41', font=('Courier', 16, 'bold')
        )
        
    def _game_loop(self):
        """Loop principal del juego"""
        self._update()
        self._draw()
        
        # Reiniciar con R
        if self.game_over and self.keys.get('r', False):
            self.__init__(self.root)
            return
            
        self.root.after(int(1000 / FPS), self._game_loop)