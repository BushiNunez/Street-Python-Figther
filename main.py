"""Punto de entrada del juego"""
import tkinter as tk
from src.game import Game

def main():
    """Ejecutar el juego"""
    root = tk.Tk()
    game = Game(root)
    root.mainloop()

if __name__ == "__main__":
    main()