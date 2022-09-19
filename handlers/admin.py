import random
from aiogram import types, Dispatcher
from config import bot, ADMINS, dp
from database.bot_db import sql_command_get_all_id


async def distribution(message: types.Message):
    if not message.from_user.id:

def register_handlers_admin(dp: Dispatcher):
    pass
