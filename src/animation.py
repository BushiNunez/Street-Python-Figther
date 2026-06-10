"""Controlador de animaciones para personajes"""
import pygame
import os
from constants import (
    ANIMATION_FRAME_SPEED, WALK_FRAMES, IDLE_FRAMES, 
    PUNCH_FRAMES, KICK_FRAMES
)

# Tamaño objetivo para los sprites (ancho x alto en píxeles)
SPRITE_WIDTH = 150
SPRITE_HEIGHT = 150


class AnimationController:
    """
    Gestiona animaciones frame-by-frame para personajes.
    Carga imágenes individuales y las cicla según el estado actual.
    """
    
    def __init__(self, character_name="Green-snake"):
        """
        Inicializar el controlador de animaciones.
        
        Args:
            character_name: Nombre base del personaje (ej: "Green-snake", "Orange-snake")
        """
        self.character_name = character_name
        self.sprites = {}
        self.frame_counter = 0
        self.current_frame = 0
        
        # Diccionario que mapea estados a listas de imágenes
        self.animations = {
            'idle': [],
            'walk': [],
            'punch': [],
            'kick': []
        }
        
        self._load_sprites()
    
    def _scale_image(self, image):
        """Escalar imagen a tamaño consistente"""
        return pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))
    
    def _load_sprites(self):
        """Cargar todas las imágenes PNG del personaje desde assets/sprites/"""
        base_path = "assets/sprites"
        
        try:
            # Cargar idle (una sola imagen)
            idle_path = f"{base_path}/{self.character_name}-idle.png"
            if os.path.exists(idle_path):
                img = pygame.image.load(idle_path).convert_alpha()
                self.animations['idle'].append(self._scale_image(img))
                print(f"✅ Cargado: idle")
            else:
                print(f"⚠️ No encontrado: {idle_path}")
            
            # Cargar walk frames (walk-1.png, walk-2.png, ..., walk-6.png)
            for i in range(1, WALK_FRAMES + 1):
                walk_path = f"{base_path}/{self.character_name}-walk-{i}.png"
                if os.path.exists(walk_path):
                    img = pygame.image.load(walk_path).convert_alpha()
                    self.animations['walk'].append(self._scale_image(img))
                else:
                    print(f"⚠️ No encontrado: {walk_path}")
            
            if self.animations['walk']:
                print(f"✅ Cargados: {len(self.animations['walk'])} frames de walk")
            
            # Cargar punch (una sola imagen)
            punch_path = f"{base_path}/{self.character_name}-punch.png"
            if os.path.exists(punch_path):
                img = pygame.image.load(punch_path).convert_alpha()
                self.animations['punch'].append(self._scale_image(img))
                print(f"✅ Cargado: punch")
            else:
                print(f"⚠️ No encontrado: {punch_path}")
            
            # Cargar kick (una sola imagen)
            kick_path = f"{base_path}/{self.character_name}-kick.png"
            if os.path.exists(kick_path):
                img = pygame.image.load(kick_path).convert_alpha()
                self.animations['kick'].append(self._scale_image(img))
                print(f"✅ Cargado: kick")
            else:
                print(f"⚠️ No encontrado: {kick_path}")
            
            print(f"\n✅ Animaciones cargadas para {self.character_name} ({SPRITE_WIDTH}x{SPRITE_HEIGHT}px)\n")
            
        except Exception as e:
            print(f"❌ Error cargando sprites de {self.character_name}: {e}")
    
    def get_frame(self, state, facing_right=True):
        """
        Obtener el frame actual para un estado dado.
        
        Args:
            state: Estado del personaje ('idle', 'walk', 'punch', 'kick')
            facing_right: Si el personaje mira a la derecha
            
        Returns:
            pygame.Surface con la imagen, o None si no hay animación para ese estado
        """
        if state not in self.animations:
            return None
        
        frames = self.animations[state]
        if not frames:
            return None
        
        # Obtener el frame actual (ciclando entre los disponibles)
        frame_index = self.current_frame % len(frames)
        sprite = frames[frame_index]
        
        # Voltear si es necesario
        if not facing_right:
            sprite = pygame.transform.flip(sprite, True, False)
        
        return sprite
    
    def update(self):
        """Actualizar el contador de frames de animación"""
        self.frame_counter += 1
        
        # Cambiar de frame cada ANIMATION_FRAME_SPEED game frames
        if self.frame_counter >= ANIMATION_FRAME_SPEED:
            self.frame_counter = 0
            self.current_frame += 1
    
    def reset_animation(self):
        """Resetear el contador de animación (para cambios de estado)"""
        self.current_frame = 0
        self.frame_counter = 0
    
    def set_frame(self, frame_number):
        """Establecer manualmente el frame actual"""
        self.current_frame = frame_number
        self.frame_counter = 0