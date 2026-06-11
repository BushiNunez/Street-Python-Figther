import os

def organizar_y_limpiar_sprites(carpeta):
    # Verificar si la carpeta realmente existe antes de continuar
    if not os.path.exists(carpeta):
        print(f"❌ La carpeta {carpeta} no existe. Verifica la ruta.")
        return

    print(f"Iniciando el proceso de reemplazo en: {carpeta}\n" + "-"*50)
    
    # Listar todos los archivos actuales de la carpeta
    archivos = os.listdir(carpeta)
    contador = 0

    for archivo in archivos:
        # Buscamos únicamente los archivos procesados (transparentes)
        if archivo.endswith("_transparent.png"):
            
            # Calculamos cuál es el nombre original (ej: de "Green-snake-idle_transparent.png" a "Green-snake-idle.png")
            nombre_original = archivo.replace("_transparent.png", ".png")
            
            # Construimos las rutas completas en el sistema
            ruta_transparente = os.path.join(carpeta, archivo)
            ruta_original = os.path.join(carpeta, nombre_original)

            try:
                # 1. Si el archivo original con fondo existe, lo eliminamos
                if os.path.exists(ruta_original):
                    os.remove(ruta_original)
                
                # 2. Renombramos el archivo transparente para que ocupe el lugar del original
                os.rename(ruta_transparente, ruta_original)
                
                print(f"🔄 Reemplazado: {archivo} ➡️ {nombre_original}")
                contador += 1
                
            except Exception as e:
                print(f"❌ Error al procesar {archivo}: {e}")

    print("-" * 50)
    print(f"✨ ¡Proceso completado! Se eliminaron los originales antiguos y se renombraron {contador} imágenes transparentes.")

# --- EJECUCIÓN ---
# Usamos la ruta exacta de tu proyecto
carpeta_sprites = "/home/andre/Curso_Python_Stanford/Street-Python-Figther/assets/sprites"
organizar_y_limpiar_sprites(carpeta_sprites)