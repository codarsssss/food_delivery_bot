import sqlite3


def start_base():
    global base, cur
    base = sqlite3.connect('data_base.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS {}(name PRIMARY KEY, description, volume, img)'.format('menu'))
    base.execute('CREATE TABLE IF NOT EXISTS {}(number, id, username, phone, address, order_size)'.format('clients'))
    base.execute('CREATE TABLE IF NOT EXISTS {}(name PRIMARY KEY, img, description)'.format('new_year_menu'))
    cur.execute('DELETE FROM menu')
    cur.execute('DELETE FROM new_year_menu')
    base.commit()
    print('БД подключена')


def upgrade_menu(name, description, volume, img):
    cur.execute('INSERT INTO menu VALUES(?,?,?,?)', (name, description, volume, img,))
    base.commit()


def upgrade_new_year_menu(name, img, description):
    cur.execute('INSERT INTO new_year_menu VALUES(?,?,?)', (name, img, description,))
    base.commit()


def get_menu():
    answer = cur.execute('SELECT * FROM menu').fetchall()
    base.commit()
    return answer


def get_menu_new_year():
    answer = cur.execute('SELECT * FROM new_year_menu').fetchall()
    base.commit()
    return answer


def show_menu(index):
    answer = cur.execute('SELECT name, volume FROM menu').fetchall()
    menu = ''

    for foo in answer:
        menu += f'{foo[0]} - {foo[1].split("Объем:")[index]}\n'

    return menu


def add_clients(number, user_id, user_name, phone, address, order_size):
    cur.execute('INSERT INTO clients VALUES(?,?,?,?,?,?)', (number, user_id, user_name, phone, address, order_size,))
    base.commit()


def add_client_phone(phone, user_id):
    cur.execute('UPDATE clients SET phone == ? WHERE id == ?', (phone, user_id,))
    base.commit()


def add_client_address(address, user_id):
    cur.execute('UPDATE clients SET address == ? WHERE id == ?', (address, user_id,))
    base.commit()


def get_client_phone(user_id):
    answer = cur.execute('SELECT phone FROM clients WHERE id == ?', (user_id,)).fetchall()
    return answer[-1][0]


def get_price_order(user_id):
    answer = cur.execute('SELECT order_size FROM clients WHERE id == ?', (user_id,)).fetchall()
    return answer[-1][0]


def get_user_id(number):
    answer = cur.execute('SELECT id FROM clients WHERE number == ?', (number,)).fetchone()
    return answer[0]


def get_all_users_id():
    answer = cur.execute('SELECT id FROM clients').fetchall()
    all_id = [i[0] for i in answer]
    return all_id


def get_user_in_base(user_id):
    answer = cur.execute('SELECT order_size, phone, address FROM clients WHERE id == ?', (user_id,)).fetchall()
    return answer[-1]


def get_number():
    answer = cur.execute('SELECT * FROM clients').fetchall()
    return len(answer)
