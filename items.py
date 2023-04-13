from aiogram import types
from database import get_all_users_id
import other


def create_main_buttons(user_id):
    try:
        markup = types.InlineKeyboardMarkup(row_width=True)
        touch_new_year = types.InlineKeyboardButton('Новогоднее предложение 🎄', callback_data='new_year')
        touch_menu = types.InlineKeyboardButton('Актуальное меню 🍲🥗🍖', callback_data='menu')
        touch_reorder = types.InlineKeyboardButton('Повторить заказ ✅', callback_data='reorder')
        touch_order = types.InlineKeyboardButton('Заказать 🚚', callback_data='order')
        touch_about = types.InlineKeyboardButton('О нас 🤩', callback_data='about')
        if other.flag:
            markup.add(touch_new_year)
        if user_id.chat.id in get_all_users_id():
            markup.add(touch_menu, touch_reorder, touch_order, touch_about)
            return markup
        markup.add(touch_menu, touch_order, touch_about)
        return markup
    except:
        pass


def create_order_buttons():
    try:
        markup = types.InlineKeyboardMarkup(row_width=True)
        touch_week = types.InlineKeyboardButton('Полная корзина - 5 400 руб 🧺', callback_data='5400')
        touch_month = types.InlineKeyboardButton('Половина корзины - 3 200 руб 🥡', callback_data='3200')
        touch_new_year_order = types.InlineKeyboardButton('🎅 Новогодняя корзина 🎄', callback_data='new_year_order')
        touch_back = types.InlineKeyboardButton('Назад 🔙', callback_data='back')
        markup.add(touch_week, touch_month)
        if other.flag:
            markup.add(touch_new_year_order)
        markup.add(touch_back)
        return markup
    except:
        pass


def create_choice_order_buttons(price):
    try:
        markup = types.InlineKeyboardMarkup(row_width=True)
        pay_now = types.InlineKeyboardButton('Оплатить онлайн (Будет позже ✍️!) 💳',
                                             callback_data=f'pay_online_off {price}')
        pay_when_shipping = types.InlineKeyboardButton('Оплатить при получении 💸',
                                                       callback_data=f'get_phone {price}')
        touch_back = types.InlineKeyboardButton('Назад 🔙', callback_data='order')
        markup.add(pay_now, pay_when_shipping, touch_back)
        return markup
    except:
        pass


def create_get_phone_buttons():
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        touch_phone = types.KeyboardButton('Отправить мой номер', request_contact=True)
        markup.add(touch_phone)
        return markup
    except:
        pass


def create_new_year_buttons():
    try:
        markup = types.InlineKeyboardMarkup(row_width=True)
        touch_30 = types.InlineKeyboardButton('30 число 🎉', callback_data='get_phone 9900')
        touch_31 = types.InlineKeyboardButton('31 число 🎁', callback_data='get_phone 10990')
        touch_back = types.InlineKeyboardButton('Назад 🔙', callback_data='order')
        markup.add(touch_30, touch_31, touch_back)
        return markup
    except:
        pass


def back_in_main():
    try:
        markup = types.InlineKeyboardMarkup()
        touch_site = types.InlineKeyboardButton('Наш сайт 🌐', url='https://kubanskiypovar.ru/')
        touch_back = types.InlineKeyboardButton('Назад 🔙', callback_data='back')
        markup.add(touch_site, touch_back)
        return markup
    except:
        pass


# Админская часть
def create_main_admin_buttons():
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        touch_sending = types.KeyboardButton('Сделать рассылку')
        touch_new_year_switch_on = types.KeyboardButton('Включить новогоднюю кнопку')
        touch_new_year_switch_off = types.KeyboardButton('Выключить новогоднюю кнопку')
        if other.flag:
            markup.add(touch_sending, touch_new_year_switch_off)
            return markup
        markup.add(touch_sending, touch_new_year_switch_on)
        return markup
    except:
        pass


def create_status_delivery_buttons(number):
    try:
        markup = types.InlineKeyboardMarkup(row_width=True)
        touch_delivery = types.InlineKeyboardButton('Курьер в пути', callback_data=f'delivery {number}')
        markup.add(touch_delivery)
        return markup
    except:
        pass


def create_status_ready_buttons(number):
    try:
        markup = types.InlineKeyboardMarkup(row_width=True)
        touch_ready = types.InlineKeyboardButton('Доставлен', callback_data=f'ready {number}')
        markup.add(touch_ready)
        return markup
    except:
        pass


def create_approve_sending_buttons():
    try:
        markup = types.InlineKeyboardMarkup(row_width=True)
        touch_approve = types.InlineKeyboardButton('Разослать', callback_data='sending')
        touch_remake = types.InlineKeyboardButton('Переделать', callback_data='remake')
        markup.add(touch_approve, touch_remake)
        return markup
    except:
        pass
