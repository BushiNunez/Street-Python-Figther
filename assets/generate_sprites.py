"""Script para generar sprites de serpientes en PNG"""
import pygame
import math

def create_snake_sprite(width=150, height=180, color_scheme='green'):
    """Crear sprite de serpiente"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    if color_scheme == 'green':
        main = (102, 221, 0)
        dark = (51, 153, 0)
        light = (153, 255, 0)
        accent = (255, 0, 0)
    else:  # brown/orange
        main = (255, 153, 0)
        dark = (204, 102, 0)
        light = (255, 200, 100)
        accent = (0, 100, 255)
    
    cx, cy = width // 2, height // 2
    
    # ========== CUERPO ==========
    # Vientre
    pygame.draw.ellipse(surface, (220, 220, 180), (cx - 35, cy - 10, 70, 90))
    
    # Lados del cuerpo
    pygame.draw.ellipse(surface, main, (cx - 50, cy - 15, 45, 100))
    pygame.draw.ellipse(surface, main, (cx + 5, cy - 15, 45, 100))
    
    # Músculos
    pygame.draw.line(surface, dark, (cx - 40, cy + 10), (cx - 20, cy + 10), 3)
    pygame.draw.line(surface, dark, (cx - 40, cy + 35), (cx - 20, cy + 35), 3)
    pygame.draw.line(surface, dark, (cx - 40, cy + 60), (cx - 20, cy + 60), 3)
    pygame.draw.line(surface, dark, (cx + 20, cy + 10), (cx + 40, cy + 10), 3)
    pygame.draw.line(surface, dark, (cx + 20, cy + 35), (cx + 40, cy + 35), 3)
    pygame.draw.line(surface, dark, (cx + 20, cy + 60), (cx + 40, cy + 60), 3)
    
    # ========== CINTURÓN ==========
    pygame.draw.rect(surface, accent, (cx - 40, cy + 60, 80, 15))
    pygame.draw.rect(surface, (0, 0, 0), (cx - 40, cy + 60, 80, 15), 2)
    
    # ========== PIERNAS ==========
    # Pata izquierda
    pygame.draw.ellipse(surface, main, (cx - 55, cy + 70, 22, 40))
    pygame.draw.ellipse(surface, dark, (cx - 55, cy + 70, 22, 40), 2)
    pygame.draw.circle(surface, dark, (cx - 44, cy + 110), 9)
    pygame.draw.polygon(surface, dark, [(cx - 50, cy + 110), (cx - 44, cy + 120), (cx - 38, cy + 110)])
    
    # Pata derecha
    pygame.draw.ellipse(surface, main, (cx + 33, cy + 70, 22, 40))
    pygame.draw.ellipse(surface, dark, (cx + 33, cy + 70, 22, 40), 2)
    pygame.draw.circle(surface, dark, (cx + 44, cy + 110), 9)
    pygame.draw.polygon(surface, dark, [(cx + 38, cy + 110), (cx + 44, cy + 120), (cx + 50, cy + 110)])
    
    # ========== BRAZOS ==========
    # Brazo izquierdo
    pygame.draw.circle(surface, main, (cx - 55, cy + 15), 11)
    pygame.draw.line(surface, main, (cx - 55, cy + 15), (cx - 70, cy + 30), 15)
    pygame.draw.circle(surface, dark, (cx - 70, cy + 30), 12)
    pygame.draw.circle(surface, (150, 150, 150), (cx - 70, cy + 30), 8)
    
    # Brazo derecho
    pygame.draw.circle(surface, main, (cx + 55, cy + 15), 11)
    pygame.draw.line(surface, main, (cx + 55, cy + 15), (cx + 70, cy + 30), 15)
    pygame.draw.circle(surface, dark, (cx + 70, cy + 30), 12)
    pygame.draw.circle(surface, (150, 150, 150), (cx + 70, cy + 30), 8)
    
    # ========== CUELLO ==========
    pygame.draw.ellipse(surface, main, (cx - 25, cy - 50, 50, 35))
    pygame.draw.ellipse(surface, dark, (cx - 25, cy - 50, 50, 35), 2)
    
    # ========== CABEZA ==========
    head_y = cy - 100
    
    # Cráneo base
    pygame.draw.ellipse(surface, main, (cx - 45, head_y - 25, 90, 65))
    pygame.draw.ellipse(surface, dark, (cx - 45, head_y - 25, 90, 65), 3)
    
    # Mandíbula
    pygame.draw.polygon(surface, main, [
        (cx - 35, head_y + 35),
        (cx + 35, head_y + 35),
        (cx + 38, head_y + 48),
        (cx - 38, head_y + 48)
    ])
    
    # Paladar
    pygame.draw.polygon(surface, (220, 220, 180), [
        (cx - 25, head_y + 24),
        (cx + 25, head_y + 24),
        (cx + 22, head_y + 38),
        (cx - 22, head_y + 38)
    ])
    
    # Colmillos
    pygame.draw.polygon(surface, (255, 255, 255), [
        (cx - 15, head_y + 24),
        (cx - 20, head_y + 42),
        (cx - 10, head_y + 32)
    ])
    pygame.draw.polygon(surface, (255, 255, 255), [
        (cx + 15, head_y + 24),
        (cx + 20, head_y + 42),
        (cx + 10, head_y + 32)
    ])
    
    # Escamas
    pygame.draw.line(surface, dark, (cx - 40, head_y - 5), (cx - 15, head_y + 10), 3)
    pygame.draw.line(surface, dark, (cx + 40, head_y - 5), (cx + 15, head_y + 10), 3)
    
    # OJOS
    pygame.draw.ellipse(surface, (255, 255, 0), (cx - 20, head_y - 15, 26, 18))
    pygame.draw.ellipse(surface, (0, 0, 0), (cx - 16, head_y - 11, 12, 10))
    pygame.draw.circle(surface, (255, 255, 0), (cx - 12, head_y - 8), 3)
    
    pygame.draw.ellipse(surface, (255, 255, 0), (cx - 6, head_y - 15, 26, 18))
    pygame.draw.ellipse(surface, (0, 0, 0), (cx - 2, head_y - 11, 12, 10))
    pygame.draw.circle(surface, (255, 255, 0), (cx + 2, head_y - 8), 3)
    
    # Nariz
    pygame.draw.polygon(surface, dark, [
        (cx, head_y - 2),
        (cx - 5, head_y + 5),
        (cx + 5, head_y + 5)
    ])
    
    # ========== CRESTA ==========
    crest_y = head_y - 28
    for i in range(5):
        crest_x = cx - 30 + (i * 15)
        pygame.draw.polygon(surface, accent, [
            (crest_x, crest_y),
            (crest_x - 8, crest_y - 20),
            (crest_x + 8, crest_y - 20)
        ])
        pygame.draw.line(surface, (0, 0, 0), 
                        (crest_x - 8, crest_y - 20),
                        (crest_x + 8, crest_y - 20), 2)
    
    return surface

def create_punch_sprite(width=150, height=180, color_scheme='green'):
    """Crear sprite de serpiente con puño extendido"""
    surface = create_snake_sprite(width, height, color_scheme)
    
    if color_scheme == 'green':
        main = (102, 221, 0)
        dark = (51, 153, 0)
    else:
        main = (255, 153, 0)
        dark = (204, 102, 0)
    
    cx, cy = width // 2, height // 2
    
    # Extender brazo derecho mucho más
    pygame.draw.line(surface, main, (cx + 55, cy + 15), (cx + 90, cy + 35), 18)
    pygame.draw.circle(surface, dark, (cx + 90, cy + 35), 14)
    pygame.draw.circle(surface, (150, 150, 150), (cx + 90, cy + 35), 10)
    
    return surface

def create_kick_sprite(width=150, height=180, color_scheme='green'):
    """Crear sprite de serpiente pateando"""
    surface = create_snake_sprite(width, height, color_scheme)
    
    if color_scheme == 'green':
        main = (102, 221, 0)
        dark = (51, 153, 0)
    else:
        main = (255, 153, 0)
        dark = (204, 102, 0)
    
    cx, cy = width // 2, height // 2
    
    # Extender pierna derecha
    pygame.draw.ellipse(surface, main, (cx + 35, cy + 65, 20, 50))
    pygame.draw.ellipse(surface, dark, (cx + 35, cy + 65, 20, 50), 2)
    pygame.draw.circle(surface, dark, (cx + 45, cy + 115), 11)
    pygame.draw.polygon(surface, dark, [(cx + 40, cy + 115), (cx + 45, cy + 130), (cx + 50, cy + 115)])
    
    return surface

def main():
    """Generar todos los sprites"""
    pygame.init()
    
    print("Generando sprites...")
    
    # Verde (Jugador)
    sprites_green = {
        'idle': create_snake_sprite(150, 180, 'green'),
        'punch': create_punch_sprite(150, 180, 'green'),
        'kick': create_kick_sprite(150, 180, 'green'),
    }
    
    # Naranja (Enemigo)
    sprites_orange = {
        'idle': create_snake_sprite(150, 180, 'orange'),
        'punch': create_punch_sprite(150, 180, 'orange'),
        'kick': create_kick_sprite(150, 180, 'orange'),
    }
    
    # Guardar imágenes
    pygame.image.save(sprites_green['idle'], 'assets/sprites/snake_green_idle.png')
    pygame.image.save(sprites_green['punch'], 'assets/sprites/snake_green_punch.png')
    pygame.image.save(sprites_green['kick'], 'assets/sprites/snake_green_kick.png')
    
    pygame.image.save(sprites_orange['idle'], 'assets/sprites/snake_orange_idle.png')
    pygame.image.save(sprites_orange['punch'], 'assets/sprites/snake_orange_punch.png')
    pygame.image.save(sprites_orange['kick'], 'assets/sprites/snake_orange_kick.png')
    
    print("✅ Sprites generados en assets/sprites/")
    pygame.quit()

if __name__ == "__main__":
    main()