from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot
from keyboard.client_cb import menu_markup, cancel_markup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    type = State()
    price = State()
    description = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.photo.set()
        await message.answer(f'Че тааам {message.from_user.username}?')
        await message.answer(f'Фотку блюда на базу 🖼️', reply_markup=cancel_markup)
    else:
        await message.answer('Малсынбы в группе меню придумывать 😤')


id = 0


async def load_photo(message: types.Message, state: FSMContext):
    global id
    async with state.proxy() as data:
        data['id'] = id
        id += 1
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer('Эми названия блюда надо ✒', reply_markup=cancel_markup)


async def load_name(message: types.Message, state: FSMContext):
    try:
        if len(message.text) > 20:
            raise ValueError
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.answer('Нужно теперь выбрать тип', reply_markup=menu_markup)
    except:
        await message.answer('Как гость будет это читать 🤬')

async def load_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text
    await FSMAdmin.next()
    await message.answer('Теперь цена сие шедевра равна 💸', reply_markup=cancel_markup)


async def load_price(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
        if price <= 0:
            raise ValueError
        if price > 1000:
            raise AttributeError
        async with state.proxy() as data:
            data['price'] = str(price)+" сом"
        await FSMAdmin.next()
        skip_button = KeyboardButton("Лень придумывать")
        skip_markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
        ).add(skip_button)
        await message.answer('Описание керекта', reply_markup=skip_markup)
    except TypeError:
        await message.answer('Мал нормально пиши')
    except ValueError:
        await message.answer("Такой цены не бывает")
    except AttributeError:
        await message.answer("Анда акча болбойт бизде")


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await bot.send_photo(message.from_user.id, data['photo'],
                       caption=f"Мына сага щедевр:\n{data['name']}, {data['type']} стоит: {data['price']}\n"
                               f"{data['description']}")
    await state.finish()
    await message.answer('Жарайсын жигар!')


async def cancel_menu_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Ну и пошел ты')


def register_handlers_fsm_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_menu_reg, state='*', commands=['cancel'], commands_prefix='\!.')
    dp.register_message_handler(cancel_menu_reg,
                                Text(equals='cancel', ignore_case=True),state='*')
    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_type, state=FSMAdmin.type)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
