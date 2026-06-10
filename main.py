"""Punto de entrada del juego Street Python Fighter"""
import sys
from pathlib import Path

# Agregar 'src' al path para que encuentre los módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

from game import Game


def main():
    """Ejecutar el juego"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()