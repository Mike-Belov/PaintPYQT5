from tkinter import colorchooser

def choose_color():
    """Открываем диалоговое окно выбора цвета"""
    color = colorchooser.askcolor(title="Выберите цвет")
    if color[1]:
        print(f"HEX: {color[1]}, RGB: {color[0]}")