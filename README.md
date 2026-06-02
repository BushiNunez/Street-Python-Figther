# Street Python Fighter Game 🥋

Un juego tipo Street Fighter hecho en Python con Tkinter como proyecto final de **Code in Place de Stanford**.

## 🎮 Descripción

Street Fighter es un juego de lucha 2D donde compites contra una IA enemiga. Usa estrategia, timing y combinaciones de ataques para vencer al oponente antes de que agote tu salud.

## ✨ Características

- 🎯 Jugador completamente controlable
- 🤖 Enemigo con IA inteligente que se adapta
- ❤️ Sistema de salud con barra visual
- 👊 Dos tipos de ataques (puñetazo y patada) con daño diferente
- 🏃 Movimiento fluido en 2D
- 🎨 Interfaz clara y responsive
- 🔄 Sistema de reinicio rápido

## 📋 Requisitos

- **Python 3.7+**
- **Tkinter** (incluido por defecto en Python)
- Sistema operativo: Windows, macOS o Linux

## 🚀 Instalación

### Opción 1: Clonar desde GitHub
```bash
git clone https://github.com/TU_USUARIO/street-fighter-game.git
cd street-fighter-game
```

### Opción 2: Descargar ZIP
1. Ve a https://github.com/TU_USUARIO/street-fighter-game
2. Click en "Code" → "Download ZIP"
3. Extrae el archivo

### Verificar dependencias (opcional)
```bash
pip install -r requirements.txt
```

## 🎮 Cómo Jugar

```bash
python main.py
```

El juego se abrirá en una ventana nueva. ¡A jugar!

## ⌨️ Controles

| Acción | Tecla |
|--------|-------|
| Mover Izquierda | **A** o **←** |
| Mover Derecha | **D** o **→** |
| Puñetazo | **Z** |
| Patada | **X** |
| Reiniciar | **R** (después de ganar/perder) |

## 🎯 Gameplay

### Objetivo
Reduce la salud del enemigo a 0 antes de que reduzca la tuya a 0.

### Mecánicas
- **Salud**: Ambos personajes comienzan con 100 HP
- **Puñetazo**: Inflige 10 de daño, rango corto
- **Patada**: Inflige 15 de daño, rango medio
- **Distancia**: Debes estar lo suficientemente cerca para que tus ataques conecten
- **IA del Enemigo**: 
  - Se persigue a ti cuando estás lejos
  - Ataca aleatoriamente cuando está lo suficientemente cerca
  - Patrón predecible (bueno para principiantes)

### Estrategia
1. Mantén distancia si tu salud es baja
2. Acércate cuando veas que el enemigo no ataca
3. Alterna puñetazos y patadas
4. Esquiva moviendo a los lados

## 📁 Estructura del Proyecto