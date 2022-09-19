import random
from aiogram import types, Dispatcher
from config import bot, ADMINS, dp
from database.bot_db import sql_command_get_all_id


async def distribution(message: types.Message):
    if not message.from_user.id in ADMINS:
        await message.reply("Ты не мой босс")
    else:
        result = await sql_command_get_all_id()
        for id in result:
            await bot.send_message(id[0], message.text.replace("/R", ""))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(distribution, commands=["R"])
