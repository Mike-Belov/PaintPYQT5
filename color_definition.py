import webcolors
from deep_translator import GoogleTranslator

def color_definition(color: tuple) -> str:
    """Опеределение цвета"""
    translator = GoogleTranslator(source='auto', target='ru')
    try: color_conclusion = translator.translate(webcolors.hex_to_name(color))
    except: color_conclusion ="Цвет не найден"
    return color_conclusion