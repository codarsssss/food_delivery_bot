from datetime import datetime, timedelta


def check_status():
    with open('new_year_status', 'r') as status:
        answer = bool(int(status.read()))
    return answer


def change_status(x):
    with open('new_year_status', 'r+') as info:
        info.write(x)


def count_date():
    week_list = ['в понедельник', 'во вторник', 'в среду', 'в четверг', 'в пятницу']
    today_index = datetime.today().weekday()
    delivery_date = datetime.today() + timedelta(days=1)
    diff_index = 0
    if today_index == 4:
        delivery_date = datetime.today() + timedelta(days=3)
    elif today_index == 5:
        delivery_date = datetime.today() + timedelta(days=2)
    elif today_index == 6:
        diff_index = 0
    else:
        diff_index = today_index + 1
    return week_list[diff_index], delivery_date.strftime("%d.%m")


flag = check_status()
