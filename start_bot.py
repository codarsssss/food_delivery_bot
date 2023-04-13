from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin
from database import start_base, upgrade_menu, upgrade_new_year_menu
from parser_menu import get_from_site


if __name__ == '__main__':
    start_base()
    info = get_from_site()
    for i in info[0]:
        upgrade_menu(i['name'], i['description'], i['volume'], i['img'])
    for i in info[1]:
        upgrade_new_year_menu(i['name'], i['img'], i['description'])
    admin.admin_register_handlers(dp)
    client.client_register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
