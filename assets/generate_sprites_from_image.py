"""Generador de sprites basado en imagen descargada de serpiente"""
from PIL import Image, ImageDraw
import os

# Crear carpeta si no existe
os.makedirs('assets/sprites', exist_ok=True)

def load_and_create_sprites():
    """Crear sprites basados en la imagen subida"""
    
    # Intentar cargar desde diferentes rutas
    posibles_rutas = [
        'assets/Serpiente_verde.png',
        './assets/Serpiente_verde.png',
        '../assets/Serpiente_verde.png',
        '/home/andre/Curso_Python_Stanford/Street-Python-Figther/assets/Serpiente_verde.png'
    ]
    
    original = None
    ruta_encontrada = None
    
    for ruta in posibles_rutas:
        try:
            original = Image.open(ruta).convert_alpha()
            ruta_encontrada = ruta
            print(f"✅ Imagen cargada desde: {ruta_encontrada}")
            print(f"   Tamaño: {original.size}")
            break
        except:
            continue
    
    if original is None:
        print("⚠️ No se encontró Serpiente_verde.png en ninguna ubicación")
        print("\nUbicaciones buscadas:")
        for ruta in posibles_rutas:
            print(f"  - {ruta}")
        print("\nVerifica que el archivo esté en assets/Serpiente_verde.png")
        return False
    
    # Redimensionar a tamaño consistente
    original = original.resize((250, 300), Image.Resampling.LANCZOS)
    
    # ========== SPRITE IDLE (Sin cambios) ==========
    sprite_idle = original.copy()
    sprite_idle.save('assets/sprites/snake_green_idle.png')
    print("✅ snake_green_idle.png creado")
    
    # ========== SPRITE PUNCH (Brazo extendido) ==========
    sprite_punch = sprite_idle.copy()
    draw_punch = ImageDraw.Draw(sprite_punch)
    
    # Dibujar brazo extendido (línea gruesa + círculo para puño)
    # Aproximadamente donde está el brazo derecho
    draw_punch.line([(160, 100), (220, 90)], fill=(102, 221, 0), width=25)
    draw_punch.ellipse([(210, 75), (240, 105)], fill=(51, 153, 0), outline=(0, 0, 0), width=2)
    draw_punch.ellipse([(215, 80), (235, 100)], fill=(150, 150, 150), outline=(0, 0, 0), width=1)
    
    sprite_punch.save('assets/sprites/snake_green_punch.png')
    print("✅ snake_green_punch.png creado")
    
    # ========== SPRITE KICK (Pierna extendida) ==========
    sprite_kick = sprite_idle.copy()
    draw_kick = ImageDraw.Draw(sprite_kick)
    
    # Dibujar pierna extendida hacia adelante
    # Aproximadamente donde está la pierna derecha
    draw_kick.line([(180, 220), (240, 260)], fill=(102, 221, 0), width=20)
    draw_kick.ellipse([(225, 245), (250, 275)], fill=(51, 153, 0), outline=(0, 0, 0), width=2)
    
    sprite_kick.save('assets/sprites/snake_green_kick.png')
    print("✅ snake_green_kick.png creado")
    
    # ========== CREAR VERSIÓN NARANJA/ENEMIGO ==========
    # Versión espejada y con colores modificados
    
    # Espejad para enemigo
    enemy_idle = original.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    
    # Modificar colores: verde -> naranja
    pixels = enemy_idle.load()
    width, height = enemy_idle.size
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # Si es verde, convertir a naranja
            if g > 150 and r < 150 and b < 150:  # Es verde
                # Verde claro -> Naranja claro
                if g > 200:
                    pixels[x, y] = (255, 200, 100, a)
                # Verde normal -> Naranja normal
                else:
                    pixels[x, y] = (255, 153, 0, a)
            
            # Si es verde oscuro, convertir a naranja oscuro
            elif g > 100 and r < 100 and b < 100:
                pixels[x, y] = (204, 102, 0, a)
    
    enemy_idle.save('assets/sprites/snake_orange_idle.png')
    print("✅ snake_orange_idle.png creado")
    
    # ========== PUNCH ENEMIGO ==========
    enemy_punch = enemy_idle.copy()
    draw_punch_enemy = ImageDraw.Draw(enemy_punch)
    
    # Brazo extendido del lado opuesto (es espejado)
    draw_punch_enemy.line([(90, 100), (30, 90)], fill=(255, 153, 0), width=25)
    draw_punch_enemy.ellipse([(10, 75), (40, 105)], fill=(204, 102, 0), outline=(0, 0, 0), width=2)
    draw_punch_enemy.ellipse([(15, 80), (35, 100)], fill=(150, 150, 150), outline=(0, 0, 0), width=1)
    
    enemy_punch.save('assets/sprites/snake_orange_punch.png')
    print("✅ snake_orange_punch.png creado")
    
    # ========== KICK ENEMIGO ==========
    enemy_kick = enemy_idle.copy()
    draw_kick_enemy = ImageDraw.Draw(enemy_kick)
    
    draw_kick_enemy.line([(70, 220), (10, 260)], fill=(255, 153, 0), width=20)
    draw_kick_enemy.ellipse([(0, 245), (25, 275)], fill=(204, 102, 0), outline=(0, 0, 0), width=2)
    
    enemy_kick.save('assets/sprites/snake_orange_kick.png')
    print("✅ snake_orange_kick.png creado")
    
    print("\n✅ ¡Todos los sprites generados correctamente!")
    print("📁 Ubicación: assets/sprites/")
    return True

if __name__ == "__main__":
    print("Generando sprites desde imagen...")
    load_and_create_sprites()   