import telebot
from datetime import datetime


def take_date(input_date):
    if input_date not in ["today", "tomorrow"]:
        # проверка на правильность введеной даты
        date = ''
        prove = input_date.split('.')

        if len(prove) == 3:
            item = ''.join(prove)
            count_digit = 0

            for x in item:
                if x.isdigit():
                    count_digit += 1

            if count_digit == 8:
                print('Дата введена верно')
                date = input_date
            else:
                print("Ошибка ввода даты")
        else:
            print("Ошибка ввода даты")

    else:
        # перевод слова в дату
        date = '.'.join(list(reversed(str(datetime.now())[:10].split('-'))))
        if input_date == 'tomorrow':
            date_list = date.split('.')
            if date_list[0] == 31 and date_list[1] in ['01', '03', '05', '07', '08', '10', '12']:
                date_list[0] = '01'
                if date_list[1] == '12':
                    date_list[1] = '01'
                    date_list[2] = str(int(date_list[2]) + 1)
                else:
                    date_list[1] = str(int(date_list[1]) + 1)

            elif date_list[0] == 30 and date_list[1] in ['04', '06', '09', '11']:
                date_list[0] = '01'
                if date_list[1] == '12':
                    date_list[1] = '01'
                    date_list[2] = str(int(date_list[2]) + 1)
                else:
                    date_list[1] = str(int(date_list[1]) + 1)

            elif date_list[1] == '02' and int(date_list[2]) % 4 == 0 and date_list[0] % 4 == '29':
                date_list[0] = '01'
                date_list[1] = '03'
            elif date_list[1] == '02' and int(date_list[2]) % 4 != 0 and date_list[0] % 4 == '28':
                date_list[0] = '01'
                date_list[1] = '03'

            else:
                if int(date_list[0]) < 10:
                    date_list[0] = '0' + str(int(date_list[0]) + 1)
                else:
                    date_list[0] = str(int(date_list[0]) + 1)

            date = '.'.join(date_list)

    return date


tasks = {}
hello_text = '''
Шалом, я бот ТуДу
Пиши в меня все задачи, на которые потом положишь болт ;)
Список моих команд - /help'''
Help = '''
/add - добавить задачу
/exit - выйти
/show - показать задачи
/del - удалить задачу
'''
token = 
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'START', 'Start'])
def start(message):
    bot.send_message(message.chat.id, hello_text)

@bot.message_handler(commands=['help', 'Help', 'HELP'])
def help(message):
    bot.send_message(message.chat.id, Help)


@bot.message_handler(commands=['Add', 'add', 'ADD'])
def add_request(message):
    bot.send_message(message.chat.id, 'Введите дату в формате ДД.ММ.ГГГГ и задачу через пробел (слова "today" и "tomorrow" тоже подойдут)')

    @bot.message_handler(content_types=['text'])
    def add(message):
        input_message = message.text.split(maxsplit=1)
        if len(input_message) != 2:  # проверка на правильный ввод даты и задачи в строку
            bot.send_message(message.chat.id, f'Еще раз прочитай и нормально введи ежжи')
        else:
            date = take_date(input_message[0])
            task = input_message[1]
            if date == '':  # проверка на правильный ввод даты, при любой херне функция вернет пустой символ
                bot.send_message(message.chat.id, f'Ан нет, братиш, не пойдет так, нормальную дату вводи да')
            else:
                if date in tasks:  # проверка на наличие даты в словаре
                    tasks[date].append(task)
                else:
                    tasks[date] = [task]

                bot.send_message(message.chat.id, f'Браток, все пучком, я добавил задачу "{task}" на дату {date}, как ты и просил))')
                print(message.chat.first_name)



bot.polling(none_stop=True)
