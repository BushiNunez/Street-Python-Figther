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
        
        # Fondo con efecto arcade
        self.canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill='#1a1a2e')
        
        # Línea separadora del ring
        self.canvas.create_line(
            WINDOW_WIDTH // 2, 100, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100,
            fill='#ff6b35', width=2, dash=(10, 10)
        )
        
        # Personajes (serpientes)
        self._draw_snake(self.player, '#00ff41')
        self._draw_snake(self.enemy, '#ff6b35')
        
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
            
    def _draw_snake(self, character, color):
        """Dibujar una serpiente animada"""
        head_x = character.x
        head_y = character.y
        
        # Efecto de ondulación cuando camina
        wave_offset = 0
        if character.attack_timer > 0:  # Está atacando
            wave_offset = (self.animation_frame % 10) * 3
        else:
            wave_offset = (self.animation_frame % 20) * 1.5
        
        # Dibujar segmentos de la serpiente (cuerpo)
        for i in range(SNAKE_SEGMENTS, 0, -1):
            segment_x = head_x - (i * SEGMENT_SIZE)
            # Ondulación del cuerpo
            segment_y = head_y + (10 * (i % 2)) if i % 2 == 0 else head_y - (10 * (i % 2))
            
            # Variación de tamaño (más pequeño hacia la cola)
            size = SEGMENT_SIZE - (i * 2)
            
            # Dibujar segmento como óvalo
            self.canvas.create_oval(
                segment_x - size, segment_y - size,
                segment_x + size, segment_y + size,
                fill=color, outline='#ffffff', width=2
            )
            
            # Patrón de escamas
            self.canvas.create_line(
                segment_x - size + 5, segment_y,
                segment_x + size - 5, segment_y,
                fill='#ffffff', width=1
            )
        
        # Dibujar cabeza
        head_size = SEGMENT_SIZE + 5
        self.canvas.create_oval(
            head_x - head_size, head_y - head_size,
            head_x + head_size, head_y + head_size,
            fill=color, outline='#ffffff', width=3
        )
        
        # Ojos de la serpiente
        eye_offset = 8
        if character.facing_right:
            # Ojos hacia la derecha
            eye1_x = head_x + eye_offset
            eye2_x = head_x + eye_offset
        else:
            # Ojos hacia la izquierda
            eye1_x = head_x - eye_offset
            eye2_x = head_x - eye_offset
            
        self.canvas.create_oval(
            eye1_x - 3, head_y - 5, eye1_x + 3, head_y - 1,
            fill='#ffffff'
        )
        self.canvas.create_oval(
            eye2_x - 3, head_y + 1, eye2_x + 3, head_y + 5,
            fill='#ffffff'
        )
        
        # Lengua de la serpiente (cuando ataca)
        if character.is_attacking:
            tongue_length = 20 + (self.animation_frame % 10)
            if character.facing_right:
                self.canvas.create_line(
                    head_x + head_size, head_y,
                    head_x + head_size + tongue_length, head_y,
                    fill='#ff00ff', width=2
                )
            else:
                self.canvas.create_line(
                    head_x - head_size, head_y,
                    head_x - head_size - tongue_length, head_y,
                    fill='#ff00ff', width=2
                )
        
        # Efecto de ataque (aura)
        if character.attack_timer > 5:
            aura_size = head_size + 10
            self.canvas.create_oval(
                head_x - aura_size, head_y - aura_size,
                head_x + aura_size, head_y + aura_size,
                outline='#ffff00', width=2
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