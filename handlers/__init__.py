from aiogram import Dispatcher

from handlers.menu import register_menu
from handlers.unknown_messages import register_unknown_message


def setup_handlers(dp: Dispatcher):
    register_menu(dp)
    register_unknown_message(dp)
