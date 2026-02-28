from tkinter import colorchooser
import data

def choose_color():
    """Открываем диалоговое окно выбора цвета"""
    color = colorchooser.askcolor(title="Выберите цвет")
    if color[1]:
        print(f"RGB: {color[0]}")
        data.color = color[0]