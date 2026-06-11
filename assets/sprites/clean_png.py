import os
from PIL import Image

def hacer_transparente(ruta_entrada, ruta_salida, tolerancia_color=30, umbral_oscuridad=50):
    try:
        # Abrir la imagen y asegurar que tenga canal de transparencia (RGBA)
        img = Image.open(ruta_entrada).convert("RGBA")
        datos = img.getdata()
        
        nuevos_datos = []
        
        for item in datos:
            r, g, b, a = item
            
            # Comprobar si es un tono de la escala de grises/blanco.
            es_escala_grises = abs(r - g) < tolerancia_color and abs(r - b) < tolerancia_color and abs(g - b) < tolerancia_color
            
            # Evitar borrar el color negro o grises extremadamente oscuros
            es_suficientemente_claro = r > umbral_oscuridad and g > umbral_oscuridad and b > umbral_oscuridad
            
            if es_escala_grises and es_suficientemente_claro:
                # Reemplazar por un píxel completamente transparente
                nuevos_datos.append((255, 255, 255, 0))
            else:
                # Mantener el píxel original
                nuevos_datos.append(item)
                
        # Actualizar la imagen con los nuevos datos
        img.putdata(nuevos_datos)
        
        # Guardar en formato PNG
        img.save(ruta_salida, "PNG")
        print(f"✅ ¡Listo! Guardado: {os.path.basename(ruta_salida)}")
        
    except Exception as e:
        print(f"❌ Error procesando {os.path.basename(ruta_entrada)}: {e}")


# --- CÓDIGO PARA PROCESAR TODA LA CARPETA ---

# Usamos la ruta exacta donde tienes guardados tus sprites
carpeta_sprites = "/home/andre/Curso_Python_Stanford/Street-Python-Figther/assets/sprites"

print(f"Buscando imágenes en: {carpeta_sprites}\n" + "-"*40)

# Listar todos los archivos dentro de la carpeta
archivos_en_carpeta = os.listdir(carpeta_sprites)

# Contador para saber cuántas imágenes procesamos
contador = 0

for nombre_archivo in archivos_en_carpeta:
    # Queremos archivos que sean .png, pero NO queremos procesar los que ya hicimos transparentes
    if nombre_archivo.endswith(".png") and not nombre_archivo.endswith("_transparent.png"):
        
        # Construir las rutas completas uniendo la carpeta con el nombre del archivo
        ruta_completa_entrada = os.path.join(carpeta_sprites, nombre_archivo)
        
        # Crear el nombre del nuevo archivo (ej: de "serpiente.png" a "serpiente_transparent.png")
        nombre_salida = nombre_archivo.replace(".png", "_transparent.png")
        ruta_completa_salida = os.path.join(carpeta_sprites, nombre_salida)
        
        # Llamar a la función que hace la magia
        hacer_transparente(ruta_completa_entrada, ruta_completa_salida)
        contador += 1

print("-" * 40)
print(f"🥋 ¡Proceso terminado! Se aplicó transparencia a {contador} imágenes para tu juego.")