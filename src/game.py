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
            bg='black'
        )
        self.canvas.pack()
        
        # Personajes
        self.player = Character(PLAYER_X, CHARACTER_Y, color='blue', is_player=True)
        self.enemy = Enemy(ENEMY_X, CHARACTER_Y)
        
        # Estado del juego
        self.running = True
        self.game_over = False
        self.winner = None
        
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
            if not self.player.attack_damage_dealt:  # ← NUEVO: Solo una vez por ataque
                damage = (PUNCH_DAMAGE if self.player.attack_type == 'punch' 
                    else KICK_DAMAGE)
                self.enemy.take_damage(damage)
                self.player.attack_damage_dealt = True  # ← NUEVO: Marcar que ya causó daño
                print(f"¡Golpe! Daño al enemigo: {damage}")  # ← DEBUG
            
        # Ataque del enemigo
        if self.enemy.is_attacking and distance < PUNCH_RANGE:
            if not self.enemy.attack_damage_dealt:  # ← NUEVO: Solo una vez por ataque
                damage = (PUNCH_DAMAGE if self.enemy.attack_type == 'punch' 
                    else KICK_DAMAGE)
                self.player.take_damage(damage)
                self.enemy.attack_damage_dealt = True  # ← NUEVO: Marcar que ya causó daño
                print(f"¡Golpe del enemigo! Daño al jugador: {damage}")  # ← DEBUG
            
    def _update(self):
        """Actualizar lógica del juego"""
        if self.game_over:
            return
            
        self._handle_input()
        self.player.update()
        self.enemy.update(self.player)
        self._check_collisions()
        
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
        
        # Fondo
        self.canvas.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill='black')
        
        # Personajes
        self._draw_character(self.player, 'blue')
        self._draw_character(self.enemy, 'red')
        
        # Barras de salud
        self._draw_health_bar(self.player, 20, 20, 'blue')
        self._draw_health_bar(self.enemy, WINDOW_WIDTH - 220, 20, 'red')
        
        # Controles
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30,
            text="[A/D o ←→] Mover | [Z] Puñetazo | [X] Patada",
            fill='white', font=('Arial', 10)
        )
        
        # Pantalla de fin de juego
        if self.game_over:
            self._draw_game_over()
            
    def _draw_character(self, character, color):
        """Dibujar un personaje"""
        x = character.x
        y = character.y
        size = character.size
        
        # Cuerpo
        self.canvas.create_rectangle(
            x - size, y - size, x + size, y + size,
            fill=color, outline='white', width=2
        )
        
        # Cabeza
        self.canvas.create_oval(
            x - size // 2, y - size - 20, x + size // 2, y - size,
            fill=color, outline='white', width=2
        )
        
        # Indicador de ataque
        if character.is_attacking:
            attack_label = "P" if character.attack_type == 'punch' else "K"
            self.canvas.create_text(
                x, y - size - 40,
                text=attack_label, fill='yellow',
                font=('Arial', 16, 'bold')
            )
            
    def _draw_health_bar(self, character, x, y, color):
        """Dibujar barra de salud"""
        bar_width = 200
        bar_height = 30
        health_percent = max(0, character.health / HEALTH_MAX)
        
        # Fondo rojo
        self.canvas.create_rectangle(x, y, x + bar_width, y + bar_height, fill='red')
        
        # Barra verde
        self.canvas.create_rectangle(
            x, y, x + (bar_width * health_percent), y + bar_height,
            fill='green'
        )
        
        # Borde
        self.canvas.create_rectangle(
            x, y, x + bar_width, y + bar_height,
            outline=color, width=2
        )
        
        # Texto
        self.canvas.create_text(
            x + bar_width // 2, y + bar_height // 2,
            text=f'HP: {int(character.health)}/{HEALTH_MAX}',
            fill='white', font=('Arial', 10, 'bold')
        )
        
    def _draw_game_over(self):
        """Mostrar pantalla de fin de juego"""
        self.canvas.create_rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
            fill='black', stipple='gray50'
        )
        
        if self.winner == "PLAYER":
            text = "¡GANASTE!"
            color = 'green'
        else:
            text = "¡PERDISTE!"
            color = 'red'
            
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50,
            text=text, fill=color, font=('Arial', 48, 'bold')
        )
        
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50,
            text="Presiona R para reiniciar",
            fill='white', font=('Arial', 16)
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