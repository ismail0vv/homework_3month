import random
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from config import bot, dp
from database.bot_db import sql_command_random, sql_command_select_type
from keyboard.client_cb import menu_markup
from handlers.parse import ParserNews
# @dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(f'Жакшысынарбы {message.from_user.full_name}')


# @dp.message_handler(commands=['mem'])
async def mem_command(message: types.Message):
    meme = [
        "media/mem1.jpg",
        "media/mem2.jpg",
        "media/mem3.jpg"
    ]
    photo = open(random.choice(meme), "rb")
    await bot.send_photo(message.chat.id, photo=photo)
    photo.close()


# @dp.message_handler(commands=["quiz"])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("След.", callback_data='button_call_1')
    markup.add(button_call_1)

    question = "Кто придумал C++"
    answers = [
        'Бог',
        'Никлаус Вирт',
        'Нашальникаа',
        'Бьёрн Страуструп',
        'Никлаус Вирт',
    ]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        explanation="ЕГО ПРИДУМАЛ САТАНА",
        open_period=30,
        reply_markup=markup
    )


async def pin(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Комманда должна быть ответом на сообщение!')
    else:
        await bot.pin_chat_message(message.chat.id, message.message_id)


async def show_random_dish(message: types.Message):
    await sql_command_random(message)


async def show_dish_types(message: types.Message):
    await bot.send_message(message.chat.id, 'Выберите тип', reply_markup=menu_markup)

async def show_dish_on_type(message: types.Message):
    result = await sql_command_select_type(message.text)
    if len(result) == 0:
        await message.answer('Пока таких блюд не существует добавьте с помощью комманды /reg')
    else:
        for dish in result:
            await bot.send_photo(message.chat.id, dish[0], caption=f'{dish[1]}, стоит: {dish[2]}, {dish[3]}\n{dish[4]}')


async def parser_news(message: types.Message):
    items = ParserNews.parser()
    for item in items:
        await bot.send_message(
            message.from_user.id,
            text=f"{item['link']}\n\n"
                 f"{item['title']}\n\n"
                 f"{item['date']}\n"
        )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(show_dish_on_type, Text(equals=['Салат 🥗', 'Суп 🥣', 'Горячее 🍳', 'Десерт 🍩', 'Напиток 🍺']))
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(mem_command, commands=['mem'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!')
    dp.register_message_handler(show_random_dish, commands=['get'])
    dp.register_message_handler(show_dish_types, commands=['list'])
    dp.register_message_handler(parser_news, commands=['news'])

