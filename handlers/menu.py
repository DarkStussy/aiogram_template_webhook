from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatType

from database.api.gateways import Gateway
from keyboard.inline import get_kb_menu


async def send_menu(message: types.Message, gateway: Gateway, state: FSMContext):
    await state.finish()
    user = await gateway.user.get_by_chat_id(message.chat.id)
    if user:
        await message.answer(f'Hi, {user.username}!', reply_markup=get_kb_menu())
    else:
        await message.answer('Hello!')


def register_menu(dp: Dispatcher):
    dp.register_message_handler(send_menu, commands=['start', 'menu'], state='*', chat_type=ChatType.PRIVATE)
