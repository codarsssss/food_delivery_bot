from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from create_bot import bot
from config import ADMINS_ID
from items import create_main_admin_buttons, create_approve_sending_buttons
from handlers.client import send_welcome
from database import get_all_users_id
import other


class FSMAdmin(StatesGroup):
    text_setting = State()
    ask = State()


async def welcome_admin(message: types.Message):
    try:
        if message.from_user.username in ADMINS_ID:
            await bot.send_message(message.chat.id, 'Добро пожаловать, Админ!',
                                   reply_markup=create_main_admin_buttons())
        else:
            await bot.send_message(message.chat.id, 'Доступ запрещен!')
    except:
        pass


async def manager_commands_admin(message: types.Message):
    try:
        if message.text == 'Сделать рассылку':
            await write_sending_text(message)
        elif message.text == 'Включить новогоднюю кнопку':
            other.change_status('1')
            other.flag = other.check_status()
            await bot.send_message(message.chat.id, 'Предложение активно', reply_markup=create_main_admin_buttons())
        elif message.text == 'Выключить новогоднюю кнопку':
            other.change_status('0')
            other.flag = other.check_status()
            await bot.send_message(message.chat.id, 'Предложение остановлено', reply_markup=create_main_admin_buttons())
    except:
        pass


async def write_sending_text(message: types.Message):
    try:
        await bot.send_message(message.chat.id, 'Отправьте текст для рассылки')
        await FSMAdmin.text_setting.set()
    except:
        pass


async def check_text_setting(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = message.text
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id-1,
                                    text=f'СООБЩЕНИЕ БУДЕТ ВЫГЛЯДЕТЬ ТАК:\n\n{message.text}',
                                    reply_markup=create_approve_sending_buttons())
        await FSMAdmin.ask.set()
    except:
        pass


async def manager_inline_buttons(call: types.CallbackQuery, state=FSMContext):
    try:
        if call.data == 'sending':
            async with state.proxy() as data:
                text = data['text']
                for user_id in get_all_users_id():
                    await bot.send_message(user_id, text)
            await state.finish()
            await bot.send_message(call.message.chat.id, 'Всем разослал!')
        elif call.data == 'remake':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            await write_sending_text(call.message)
    except:
        pass


def admin_register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_message_handler(welcome_admin, commands=['admin'])
    dp.register_message_handler(manager_commands_admin, content_types=['text'])
    dp.register_message_handler(check_text_setting, state=FSMAdmin.text_setting)
    dp.register_callback_query_handler(manager_inline_buttons, lambda x: x.data, state=FSMAdmin.ask)
