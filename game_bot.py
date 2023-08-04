from math import floor
from random import randint
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from requests import get
from environs import Env
import save_script
import prompts


# сохранение и загрузка данных с помощью джейсон файла
def save_data(n):
    save_script.update_data(n)


def load_data():
    d = save_script.load_from_data()
    return d

env = Env()
env.read_env()

difficults: dict = {'X': 69, 'A': 20, 'B': 15, 'C': 10, 'D': 5, 'E': 1}
API_TOKEN: str = str(env('BOT_TOKEN'))
users: dict = dict(load_data())
print(users)

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


def get_random() -> int:
    return randint(1, 100)


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    print(message.from_user.first_name)
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')
    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
    if str(message.from_user.id) not in users:
        users[str(message.from_user.id)] = {'name': message.from_user.first_name + ' ' + message.from_user.last_name
        if message.from_user.last_name else message.from_user.first_name,
                                            'in_game': False,
                                            'secret_number': None,
                                            'attempts': None,
                                            'total_games': 0,
                                            'wins': 0,
                                            'is_choise_difficulty': False,
                                            'dif_attempts': 10
                                            }
    save_data(users)
    print(str(message.from_user.id))


@dp.message(Command(commands=['cat']))
async def show_cat(message: Message):
    cat = get('https://api.thecatapi.com/v1/images/search')
    if cat.status_code == 200:
        await  message.answer_photo(cat.json()[0]['url'])
    else:
        await message.answer('Котов больше нема((')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('/rules - узнать правила\n'
                         '/game - сыграть\n'
                         '/cancel - выйти из игры\n'
                         '/stat - статистика\n'
                         '/difficulty - выбор сложности\n'
                         '/lead - таблица лидеров\n'
                         '/cat - рандомный котик')


@dp.message(Command(commands=['rules']))
async def show_rules(message: Message):
    await message.answer(f'Я загадываю число от 0 до 100\n'
                         f'попробуй угадать его за {users[str(message.from_user.id)]["dif_attempts"]} попыток')


@dp.message(Command(commands=['difficulty']))
async def choise_difficulty(message: Message):
    users[str(message.from_user.id)]['is_choise_difficulty'] = True
    await message.answer('Напиши мне букаву\n\n'
                         'Пригожин Женя (69 попыток) - X\n'
                         'Изя и Йосып (20) - A\n'
                         'Бывалый смешарик (15) - B\n'
                         'Базированный гигачад (10) - C\n'
                         'Шаша Шимпл (5) - D\n'
                         'Зачет у дзержа (1) - E\n\n'
                         '(пиши в верхнем регистре английскими буквами)')
    save_data(users)


@dp.message(lambda x: x.text and len(x.text) == 1 and x.text == x.text.upper() and x.text.isalpha())
async def change_difficulty(message: Message):
    if users[str(message.from_user.id)]['is_choise_difficulty'] and message.text in difficults.keys():

        users[str(message.from_user.id)]['dif_attempts'] = int(difficults[message.text])
        await message.answer(f'Текущая сложность: {difficults[message.text]}')
        if message.text == 'E':
            await message.answer('Ну ты зревь нахуй')
        users[str(message.from_user.id)]['is_choise_difficulty'] = False
    else:
        await message.answer('Я не вдупляю, ты хочешь сыграть?')


@dp.message(Command(commands=['stat']))
async def show_stats(message: Message):
    a = f'Всего игр сыграно: {users[str(message.from_user.id)]["total_games"]}\nПобед: {users[str(message.from_user.id)]["wins"]}\n'
    if users[str(message.from_user.id)]['total_games'] == 0:
        await message.answer(a)
    else:
        b = f'Процент побед = {floor(users[str(message.from_user.id)]["wins"] / users[str(message.from_user.id)]["total_games"] * 100)} %'
        await message.answer(a + '\n' + b)


@dp.message(Command(commands=['lead']))
async def show_leaderboard(message: Message):
    board = []
    for id, data in users.items():
        board.append(data['name'] + ' - ' + str(data['wins']) + ' - ' + str(data['total_games']))

    board.sort(key=lambda x: x.split('-')[1], reverse=True)
    for x in range(len(board)):
        board[x] = str(x + 1) + ') ' + board[x]
    print(board)

    await message.answer('Доска позора большие березники\n'
                         'Имя - Победы - Всего игр\n')
    await message.answer('\n'.join(board))


@dp.message(Command(commands=['cancel', 'exit']))
async def exit_from_game(message: Message):
    if users[str(message.from_user.id)]['in_game']:
        await message.answer('Понял, закругляемся')
        users[str(message.from_user.id)]['in_game'] = False
        users[str(message.from_user.id)]['total_games'] += 1
    else:
        await message.answer('Мы и так не играем, дядь')
    save_data(users)


@dp.message(F.text.lower().in_({'go', 'го', 'yes', 'да', 'давай', 'сыграем'}))
@dp.message(Command(commands=['game']))
async def agree_to_game(message: Message):
    if users[str(message.from_user.id)]['in_game'] == False:
        await message.answer('Приятной игры')
        await message.answer('Я загадал число от 1 до 100,'
                             'угадывай')
        users[str(message.from_user.id)]['in_game'] = True
        users[str(message.from_user.id)]['secret_number'] = get_random()
        users[str(message.from_user.id)]['attempts'] = users[str(message.from_user.id)]['dif_attempts']
    else:
        await message.answer('Мы и так играем, bruh')
    save_data(users)


@dp.message(F.text.lower().in_({'нет', 'не', 'не хочу', 'no', 'no way'}))
async def agree_to_game(message: Message):
    if users[str(message.from_user.id)]['in_game'] == False:
        await message.answer('Понял, не пристаю\nНо если что я всегда тут\nПиши ;)')
    else:
        await message.answer('Игра идет, брух\nЕсли в натуре кидок жиес, пиши /cancel')


@dp.message(lambda mes: mes.text and mes.text.isdigit() and 0 < int(mes.text) <= 100)
async def game_process(message: Message):
    if users[str(message.from_user.id)]['in_game']:
        if int(message.text) == users[str(message.from_user.id)]['secret_number']:
            await message.answer('Красавчик жи ес, угадал')
            users[str(message.from_user.id)]['wins'] += 1
            users[str(message.from_user.id)]['total_games'] += 1
            users[str(message.from_user.id)]['in_game'] = False
        elif int(message.text) < users[str(message.from_user.id)]['secret_number']:
            await message.answer('Вай эбе, мое число больше))')
            users[str(message.from_user.id)]['attempts'] -= 1
            await message.answer(f'Попыток осталось: {users[str(message.from_user.id)]["attempts"]}')
        elif int(message.text) > users[str(message.from_user.id)]['secret_number']:
            await message.answer('Загнул, дядька, я загадал число поменьше')
            users[str(message.from_user.id)]['attempts'] -= 1
            await message.answer(f'Попыток осталось: {users[str(message.from_user.id)]["attempts"]}')

        if users[str(message.from_user.id)]['attempts'] == 0:
            await message.answer('Проиграл, дядя, сымай штаны :))\n'
                                 f'Ладно, шухчу, мое число было {users[str(message.from_user.id)]["secret_number"]}')
            users[str(message.from_user.id)]['total_games'] += 1
            users[str(message.from_user.id)]['in_game'] = False

        print(users[str(message.from_user.id)])
        await prompts.prompts(message, users[str(message.from_user.id)]['secret_number'])
    else:
        await message.answer('Мы еще не играем, хочешь сыграть?')
    save_data(users)


@dp.message(F.text)
async def other_messages(message: Message):
    await message.answer('Я не вдупляю, ты хочешь сыграть?')


if __name__ == '__main__':
    dp.run_polling(bot)
