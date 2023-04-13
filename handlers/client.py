from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import GROUP_ID_ADMIN
from create_bot import bot
from pay_orders import pay_order
from items import *
from database import *
from other import count_date


class FSMClient(StatesGroup):
    application = State()


async def send_welcome(message: types.Message):
    try:
        await bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!\n'
                                                f'Я помогу Вам удобно и не дорого заказывать вкусную еду для всей '
                                                f'семьи 👨‍👩‍👧‍👦!\n'
                                                f'\nВы можете:\n'
                                                f'\n*• 🎄   заказать Новогоднее меню\n'
                                                f'\n• 🧑‍🍳   посмотреть акуальное меню на эту неделю \n'
                                                f'\n• 🛒   сделать заказ \n'
                                                f'\n• 👑   узнать подробнее о том, какие мы красавчики 🤴* \n'
                                                f'\n_Доставка по Краснодару - БЕСПЛАТНО!_', parse_mode='Markdown')
        await send_commands(message)
    except:
        pass


async def send_commands(message: types.Message):
    try:
        await bot.send_message(message.chat.id, 'Выберите, что Вас интересует:',
                               reply_markup=create_main_buttons(message))
    except:
        pass


async def manager_commands(call: types.CallbackQuery):
    try:
        if call.data == 'menu':
            for i in get_menu():
                text_menu = f'*{i[0]}*\n\nСостав: {i[1]}\n'
                await bot.send_photo(call.message.chat.id, i[3], text_menu, parse_mode='Markdown')
            await bot.send_message(call.message.chat.id, 'Выберите что Вас интересует:',
                                   reply_markup=create_main_buttons(call.message))

        elif call.data == 'order':
            if other.flag:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='*Полная корзина* - рекомендуется на недельный рацион 3-4 человек '
                                                 '👨‍👩‍👧‍👦\n '
                                                 '🏋️‍♂️Составит около 16 кг продуктов.\n'
                                                 '\n*Половина корзины* - рекомендуется на недельный рацион 1-2 человек '
                                                 '👫 \n '
                                                 '🏋️‍♂️Составит около 8 кг продуктов.\n'
                                                 '\n🎄*Новогодняя корзина* - это удобный способ организовать стол без '
                                                 'лишней суеты. Займитесь тем, что действительно важно, не отвлекаясь '
                                                 'на бытовые задачи.\n\n*Доставка еды на дом на Новый год* имеет '
                                                 'множество преимуществ, главное из которых – возможность '
                                                 'организовать разнообразный великолепный праздничный стол без '
                                                 'каких-либо усилий.\n\n*Наш шеф-повар* подготовил к Новому году '
                                                 'праздничное меню с новогодней классикой, интересными авторскими '
                                                 'закусками и высококлассными горячими блюдами.\n🎅🧑‍🎄🤶',
                                            reply_markup=create_order_buttons(), parse_mode='Markdown')
            else:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='*Полная корзина* - рекомендуется на недельный рацион 3-4 человек '
                                                 '👨‍👩‍👧‍👦\n '
                                                 '🏋️‍♂️Составит около 16 кг продуктов.\n'
                                                 '\n*Половина корзины* - рекомендуется на недельный рацион 1-2 человек '
                                                 '👫 \n '
                                                 '🏋️‍♂️Составит около 8 кг продуктов.',
                                            reply_markup=create_order_buttons(), parse_mode='Markdown')

        elif call.data.split()[0] == 'pay_online':
            if call.data.split()[1] == '3200':
                title = 'Половина корзины'
                description = 'Рекомендуем для семьи из 2-х человек'
            else:
                title = 'Полная корзина'
                description = 'Рекомендуем для семьи из 4-х человек'
            await pay_order(call.message, call.data.split()[1], title, description)

        elif call.data.split()[0] == 'get_phone':
            add_clients(get_number() + 1, call.message.chat.id, call.from_user.username, '', '', call.data.split()[1])
            await get_phone(call.message)

        elif call.data == '3200' or call.data == '5400':
            index = 1
            if call.data == '5400':
                index = 2
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=show_menu(index), reply_markup=create_choice_order_buttons(call.data))

        elif call.data == 'reorder':
            info = get_user_in_base(call.message.chat.id)
            ready_date = count_date()
            add_clients(get_number() + 1, call.message.chat.id, call.from_user.username, info[1], info[2], info[0])
            text_application = f'№ {get_number()}\nОплата - При получении\nВид - ' \
                               f'{"Половина корзины" if info[0] == "3200" else "Полная корзина"}\n' \
                               f'Клиент - @{call.from_user.username}\nТелефон - {info[1]}\nАдрес - {info[2]}'
            await bot.send_message(GROUP_ID_ADMIN, text_application,
                                   reply_markup=create_status_delivery_buttons(text_application.split()[1]))
            await bot.send_message(call.message.chat.id,
                                   f'Спасибо за заказ 😊\nПривезём {ready_date[0]} ({ready_date[1]})\nС вами '
                                   f'дополнительно свяжется менеджер!\n\n*Если хотите изменить какие-то параметры, '
                                   f'нажмите «заказать» и заполните все необходимые поля заново*',
                                   parse_mode='Markdown')
            await send_commands(call.message)

        elif call.data.split()[0] == 'delivery':
            user_id = get_user_id(int(call.data.split()[1]))
            await bot.send_message(user_id, 'Курьер едет к вам 🚚!\n*Будет в течении часа* ⏳', parse_mode='Markdown')
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text=f'ДОСТАВКА\n{call.message.text}',
                                        reply_markup=create_status_ready_buttons(call.data.split()[1]))

        elif call.data.split()[0] == 'ready':
            user_id = get_user_id(int(call.data.split()[1]))
            await bot.send_animation(user_id, 'https://media.tenor.com/oNYYcF9NzjoAAAAd/mukbang-food.gif')
            await bot.send_message(user_id, 'Заказ доставлен! Приятного аппетита!', parse_mode='Markdown')
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text=f'{call.message.text.replace("ДОСТАВКА", "ВЫДАН")}')

        elif call.data == 'about':
            with open('about.txt', 'r', encoding='utf-8') as info:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text=info.read(), reply_markup=back_in_main())

        elif call.data == 'back':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Выберите что Вас интересует:',
                                        reply_markup=create_main_buttons(call.message))

        elif call.data == 'new_year':
            new_year_menu = get_menu_new_year()
            for i in new_year_menu:
                text_menu = f'*{i[0]}*\n\n{i[2]}\n'
                await bot.send_photo(call.message.chat.id, i[1], text_menu, parse_mode='Markdown')
            await bot.send_message(call.message.chat.id, 'Стоимость зависит от даты получения,\n'
                                                         'состав корзины '
                                                         '*не меняется*\n'
                                                         '30 декабря - 9900 руб.\n'
                                                         '31 декабря - 10990 руб.', parse_mode='Markdown')
            await bot.send_message(call.message.chat.id, 'Выберите что Вас интересует:',
                                   reply_markup=create_main_buttons(call.message))

        elif call.data == 'new_year_order':
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Стоимость корзины 30 декабря - 9900 руб.\n'
                                             'Стоимость корзины 31 декабря - 10990 руб.\n'
                                             'Выберите дату доставки:',
                                        reply_markup=create_new_year_buttons())
    except:
        pass


async def get_phone(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправте номер телефона нажав кнопку на клавиатуре 📞👇',
                           reply_markup=create_get_phone_buttons())


async def get_address(message: types.Message):
    add_client_phone(message.contact.phone_number, message.chat.id)
    await bot.send_message(message.chat.id, 'Теперь напишите адрес доставки 🏚📍\n(укажите улицу, дом, подъезд, этаж, '
                                            'квартиру)\n\n`Примерно так:\nул. Новороссийская, д 240, п 1,  эт 17, '
                                            'кв 474`', reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
    await FSMClient.application.set()


async def send_application(message: types.Message, state=FSMContext):
    add_client_address(message.text, message.chat.id)
    if get_price_order(message.chat.id) == '9900' or get_price_order(message.chat.id) == '10990':
        text_application = f'№ {get_number()}\nОплата - При получении\nВид - ' \
                           f'{"Новогодняя корзина 30 число" if get_price_order(message.chat.id) == "9900" else "Новогодняя корзина 31 число"}' \
                           f'\nКлиент - @{message.from_user.username}\nТелефон - {get_client_phone(message.chat.id)}' \
                           f'\nАдрес - {message.text}'
        await bot.send_message(message.chat.id,
                               f'Спасибо за заказ 😊\nПривезём {"30 декабря" if get_price_order(message.chat.id) == "9900" else "31 декабря"}\nС вами дополнительно '
                               f'свяжется менеджер!\n\n*Теперь мы Вас знаем и чтобы повторить заказ нажмите на кнопку '
                               f'«Повторить заказ»\nЕсли хотите изменить какие-то параметры, нажмите «заказать» и '
                               f'заполните все необходимые поля заново*',
                               parse_mode='Markdown')
    else:
        text_application = f'№ {get_number()}\nОплата - При получении\nВид - ' \
                           f'{"Половина корзины" if get_price_order(message.chat.id) == "3200" else "Полная корзина"}' \
                           f'\nКлиент - @{message.from_user.username}\nТелефон - {get_client_phone(message.chat.id)}' \
                           f'\nАдрес - {message.text}'
        ready_date = count_date()
        await bot.send_message(message.chat.id,
                               f'Спасибо за заказ 😊\nПривезём {ready_date[0]} ({ready_date[1]})\nС вами дополнительно '
                               f'свяжется менеджер!\n\n*Теперь мы Вас знаем и чтобы повторить заказ нажмите на кнопку '
                               f'«Повторить заказ»\nЕсли хотите изменить какие-то параметры, нажмите «заказать» и '
                               f'заполните все необходимые поля заново*',
                               parse_mode='Markdown')
    await bot.send_message(GROUP_ID_ADMIN, text_application,
                           reply_markup=create_status_delivery_buttons(text_application.split()[1]))
    await state.finish()
    await send_commands(message)


def client_register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=['start', 'help'])
    dp.register_callback_query_handler(manager_commands, lambda x: x.data)
    dp.register_message_handler(get_phone)
    dp.register_message_handler(get_address, content_types=['contact'])
    dp.register_message_handler(send_application, state=FSMClient.application)
