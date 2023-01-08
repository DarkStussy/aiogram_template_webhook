from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_kb_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton('Menu', callback_data='menu'))
