"""Generador de imágenes PNG de alta calidad para las serpientes"""
from PIL import Image, ImageDraw
import os

os.makedirs('assets/sprites', exist_ok=True)

def draw_snake(draw, x_offset, y_offset, width, height, color_scheme='green', state='idle'):
    """Dibujar una serpiente detallada"""
    
    if color_scheme == 'green':
        main = (102, 221, 0)
        dark = (51, 153, 0)
        light = (153, 255, 0)
        accent = (255, 0, 0)
        skin = (200, 200, 150)
    else:
        main = (255, 153, 0)
        dark = (204, 102, 0)
        light = (255, 200, 100)
        accent = (0, 100, 255)
        skin = (220, 180, 120)
    
    cx = x_offset + width // 2
    cy = y_offset + height // 2
    
    # ========== COLA ==========
    tail_x = x_offset + 10
    for i in range(8):
        seg_x = tail_x + (i * 12)
        seg_y = cy + 30 + (8 if i % 2 == 0 else -8)
        radius = 12 - i
        draw.ellipse([seg_x - radius, seg_y - radius, seg_x + radius, seg_y + radius], 
                    fill=main, outline=dark, width=2)
    
    # ========== CUERPO ==========
    # Vientre
    draw.ellipse([cx - 35, cy - 10, cx + 35, cy + 90], fill=skin, outline=dark, width=2)
    
    # Lado izquierdo
    draw.ellipse([cx - 50, cy - 15, cx - 5, cy + 95], fill=main, outline=dark, width=2)
    
    # Lado derecho
    draw.ellipse([cx + 5, cy - 15, cx + 50, cy + 95], fill=main, outline=dark, width=2)
    
    # Detalles musculares
    for i in range(4):
        y_off = cy + 10 + (i * 20)
        draw.line([cx - 40, y_off, cx - 20, y_off], fill=dark, width=3)
        draw.line([cx + 20, y_off, cx + 40, y_off], fill=dark, width=3)
    
    # ========== CINTURÓN ==========
    draw.rectangle([cx - 42, cy + 60, cx + 42, cy + 75], fill=accent, outline=(0, 0, 0), width=2)
    draw.text((cx - 12, cy + 62), "P1" if color_scheme == 'green' else "P2", 
             fill=(255, 255, 0), font=None)
    
    # ========== PIERNAS ==========
    # Pierna izquierda
    draw.ellipse([cx - 55, cy + 70, cx - 33, cy + 105], fill=main, outline=dark, width=2)
    draw.ellipse([cx - 53, cy + 103, cx - 35, cy + 125], fill=main, outline=dark, width=2)
    draw.ellipse([cx - 50, cy + 118, cx - 38, cy + 132], fill=dark, outline=(0, 0, 0), width=1)
    
    # Pierna derecha
    draw.ellipse([cx + 33, cy + 70, cx + 55, cy + 105], fill=main, outline=dark, width=2)
    draw.ellipse([cx + 35, cy + 103, cx + 53, cy + 125], fill=main, outline=dark, width=2)
    draw.ellipse([cx + 38, cy + 118, cx + 50, cy + 132], fill=dark, outline=(0, 0, 0), width=1)
    
    # ========== BRAZOS ==========
    if state == 'idle':
        # Brazo izquierdo reposo
        draw.ellipse([cx - 60, cy + 10, cx - 38, cy + 32], fill=main, outline=dark, width=2)
        draw.line([cx - 55, cy + 22, cx - 70, cy + 35], fill=main, width=14)
        draw.ellipse([cx - 77, cy + 28, cx - 63, cy + 42], fill=dark, outline=(0, 0, 0), width=2)
        
        # Brazo derecho reposo
        draw.ellipse([cx + 38, cy + 10, cx + 60, cy + 32], fill=main, outline=dark, width=2)
        draw.line([cx + 55, cy + 22, cx + 70, cy + 35], fill=main, width=14)
        draw.ellipse([cx + 63, cy + 28, cx + 77, cy + 42], fill=dark, outline=(0, 0, 0), width=2)
    
    elif state == 'punch':
        # Brazo izquierdo reposo
        draw.ellipse([cx - 60, cy + 10, cx - 38, cy + 32], fill=main, outline=dark, width=2)
        draw.line([cx - 55, cy + 22, cx - 70, cy + 35], fill=main, width=14)
        draw.ellipse([cx - 77, cy + 28, cx - 63, cy + 42], fill=dark, outline=(0, 0, 0), width=2)
        
        # Brazo derecho EXTENDIDO
        draw.ellipse([cx + 38, cy + 10, cx + 60, cy + 32], fill=main, outline=dark, width=2)
        draw.line([cx + 55, cy + 22, cx + 95, cy + 32], fill=main, width=16)
        draw.ellipse([cx + 88, cy + 18, cx + 102, cy + 46], fill=dark, outline=(0, 0, 0), width=2)
        draw.ellipse([cx + 87, cy + 24, cx + 103, cy + 40], fill=(150, 150, 150), outline=(0, 0, 0))
    
    elif state == 'kick':
        # Brazos en reposo
        draw.ellipse([cx - 60, cy + 10, cx - 38, cy + 32], fill=main, outline=dark, width=2)
        draw.line([cx - 55, cy + 22, cx - 70, cy + 35], fill=main, width=14)
        draw.ellipse([cx - 77, cy + 28, cx - 63, cy + 42], fill=dark, outline=(0, 0, 0), width=2)
        
        draw.ellipse([cx + 38, cy + 10, cx + 60, cy + 32], fill=main, outline=dark, width=2)
        draw.line([cx + 55, cy + 22, cx + 70, cy + 35], fill=main, width=14)
        draw.ellipse([cx + 63, cy + 28, cx + 77, cy + 42], fill=dark, outline=(0, 0, 0), width=2)
        
        # Pierna derecha EXTENDIDA
        draw.ellipse([cx + 35, cy + 70, cx + 55, cy + 105], fill=main, outline=dark, width=2)
        draw.ellipse([cx + 37, cy + 103, cx + 55, cy + 140], fill=main, outline=dark, width=2)
        draw.ellipse([cx + 40, cy + 135, cx + 52, cy + 150], fill=dark, outline=(0, 0, 0), width=1)
    
    # ========== CUELLO ==========
    draw.ellipse([cx - 28, cy - 50, cx + 28, cy - 18], fill=main, outline=dark, width=2)
    
    # ========== CABEZA ==========
    head_y = cy - 100
    
    # Cráneo
    draw.ellipse([cx - 48, head_y - 25, cx + 48, head_y + 40], 
                fill=main, outline=dark, width=3)
    
    # Mandíbula
    draw.polygon([(cx - 38, head_y + 35), (cx + 38, head_y + 35), 
                 (cx + 42, head_y + 48), (cx - 42, head_y + 48)],
                fill=main, outline=dark)
    
    # Paladar
    draw.polygon([(cx - 28, head_y + 23), (cx + 28, head_y + 23),
                 (cx + 24, head_y + 37), (cx - 24, head_y + 37)],
                fill=skin, outline=(0, 0, 0))
    
    # Colmillos
    draw.polygon([(cx - 16, head_y + 23), (cx - 21, head_y + 42), (cx - 11, head_y + 32)],
                fill=(255, 255, 255), outline=(0, 0, 0))
    draw.polygon([(cx + 16, head_y + 23), (cx + 21, head_y + 42), (cx + 11, head_y + 32)],
                fill=(255, 255, 255), outline=(0, 0, 0))
    
    # Escamas
    draw.line([cx - 42, head_y - 8, cx - 16, head_y + 8], fill=dark, width=3)
    draw.line([cx + 42, head_y - 8, cx + 16, head_y + 8], fill=dark, width=3)
    
    # OJOS
    draw.ellipse([cx - 22, head_y - 16, cx - 8, head_y - 6], 
                fill=(255, 255, 0), outline=(0, 0, 0), width=2)
    draw.ellipse([cx - 18, head_y - 12, cx - 12, head_y - 8],
                fill=(0, 0, 0))
    draw.ellipse([cx - 14, head_y - 10, cx - 10, head_y - 6],
                fill=(255, 255, 0))
    
    draw.ellipse([cx + 8, head_y - 16, cx + 22, head_y - 6],
                fill=(255, 255, 0), outline=(0, 0, 0), width=2)
    draw.ellipse([cx + 12, head_y - 12, cx + 18, head_y - 8],
                fill=(0, 0, 0))
    draw.ellipse([cx + 10, head_y - 10, cx + 14, head_y - 6],
                fill=(255, 255, 0))
    
    # Nariz
    draw.polygon([(cx, head_y - 2), (cx - 6, head_y + 6), (cx + 6, head_y + 6)],
                fill=dark, outline=(0, 0, 0))
    
    # ========== CRESTA ==========
    crest_y = head_y - 30
    for i in range(5):
        crest_x = cx - 32 + (i * 16)
        draw.polygon([(crest_x, crest_y), (crest_x - 8, crest_y - 18), (crest_x + 8, crest_y - 18)],
                    fill=accent, outline=(0, 0, 0))

def create_image(width=200, height=240, color_scheme='green', state='idle'):
    """Crear imagen de serpiente"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_snake(draw, 0, 0, width, height, color_scheme, state)
    return img

print("Generando imágenes de alta calidad...")

# Generar imágenes para jugador (verde)
create_image(200, 240, 'green', 'idle').save('assets/sprites/snake_green_idle.png')
print("✅ snake_green_idle.png")

create_image(200, 240, 'green', 'punch').save('assets/sprites/snake_green_punch.png')
print("✅ snake_green_punch.png")

create_image(200, 240, 'green', 'kick').save('assets/sprites/snake_green_kick.png')
print("✅ snake_green_kick.png")

# Generar imágenes para enemigo (naranja)
create_image(200, 240, 'orange', 'idle').save('assets/sprites/snake_orange_idle.png')
print("✅ snake_orange_idle.png")

create_image(200, 240, 'orange', 'punch').save('assets/sprites/snake_orange_punch.png')
print("✅ snake_orange_punch.png")

create_image(200, 240, 'orange', 'kick').save('assets/sprites/snake_orange_kick.png')
print("✅ snake_orange_kick.png")

print("\n✅ ¡Todas las imágenes generadas correctamente!")
print("📁 Ubicación: assets/sprites/")