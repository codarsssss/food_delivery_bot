from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType
from create_bot import bot, dp
from config import PAY_TOKEN, GROUP_ID_ADMIN
from database import add_clients, get_number


async def pay_order(message: Message, data, title, description):
    order = [LabeledPrice(label='Подписка на еду', amount=int(data) * 100)]
    await bot.send_invoice(message.chat.id, title=title,
                           description=description,
                           provider_token=PAY_TOKEN,
                           currency='rub',
                           need_name=True,
                           need_phone_number=True,
                           prices=order,
                           payload='same')


@dp.pre_checkout_query_handler(lambda x: True)
async def check_progress(checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(checkout_query.id, ok=True)
    await bot.send_message(GROUP_ID_ADMIN,
                           f'№ {get_number()}\nОплата - ОНЛАЙН\nВид - '
                           f'{"Половина корзины" if checkout_query.total_amount // 100 == 3200 else "Полная корзина"}'
                           f'\nКлиент - @{checkout_query.from_user.username}')
    add_clients(get_number(), checkout_query.from_user.id, checkout_query.from_user.username, '8918',
                'Покрышкина', 'БОЛЬШАЯ КАРЗИНА')


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def answer_after_buy(message: Message):
    if message.from_user.username is not None:
        await bot.send_message(message.chat.id, '*Оплата прошла успешно!* Я уже передал Вашу заявку администратору. '
                                                'Он скоро с Вами свяжется! \n\nЕсли дело срочное, Вы можете '
                                                'самостоятельно написать ему 👨‍💻', parse_mode='Markdown')
    else:
        await bot.send_message(message.chat.id, '*Оплата прошла успешно!* Пожалуйста, свяжитесь с администратором '
                                                'нажатием этой кнопки ⬇', parse_mode='Markdown')
        await bot.send_message(message.chat.id, 'Что бы мы могли автоматичесски связываться в будущем, '
                                                'задайте себе имя пользователя (ссылку) в настройках '
                                                'Телеграмм 📌')
    await bot.send_message(message.from_user.id, 'С вами свяжется менеджер')
