from random import randint
from aiogram import Bot, Dispatcher
from aiogram.types import Message


API_TOKEN: str = '6348992336:AAFYCy0mXyAyZebEA9D9LkybeiCCOvHd8jQ'
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


async def first_prompt(message : Message, secret : int):
    pr = []
    for x in range(7):
        rand = randint(1,100)
        if rand != secret and rand not in pr:
            pr.append(str(rand))


    await message.answer('Siuuu, тебе попалась обычная подсказка\n'
                         'Я подскажу тебе 7 чисел, которые я точно не загадал')
    await message.answer('Вот они: ' + ' '.join(pr))


async def second_prompt(message: Message, secret: int):

    await message.answer('Вот это ништяк!!! Редкая подсказуйка')
    await message.answer(f'Нужное тебе число находится между {secret - randint(1,10)} и {secret + randint(1,10)}')


async def prompts(message : Message, secret: int):
    x = randint(1,100)
    if 1 <= x <= 20:
        await first_prompt(message, secret)
    elif 21 <= x <= 30:
        await second_prompt(message, secret)

