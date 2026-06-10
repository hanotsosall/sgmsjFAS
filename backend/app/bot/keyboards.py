from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def characters_keyboard(characters):
    buttons = []
    for char in characters:
        buttons.append([InlineKeyboardButton(text=char.name, callback_data=f"char_{char.id}")])
    buttons.append([InlineKeyboardButton(text="🛒 Магазин", callback_data="shop")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)