import random
import sqlite3
from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()
    if db:
        print('Successfully connected!')

    db.execute("CREATE TABLE IF NOT EXISTS menu "
               "(id INTEGER PRIMARY KEY, photo TEXT,"
               "name TEXT, price INTEGER,"
               "description TEXT)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO menu VALUES (?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sqL_command_random(message):
    result = cursor.execute("SELECT * FROM menu").fetchall()
    random_dish = random.choice(result)
    await bot.send_photo(message.from_user.id, random_dish[1],
                         caption=f"{random_dish[2]}, {random_dish[3]}, {random_dish[4]}")


async def sql_command_all():
    return cursor.execute("SELECT * FROM menu").fetchall()


async def sql_command_delete(id):
    cursor.execute("DELETE FROM menu WHERE id = ?", tuple(id))
    db.commit()


async def sql_command_get_all_id():
    return cursor.execute("SELECT id FROM menu").fetchall()
