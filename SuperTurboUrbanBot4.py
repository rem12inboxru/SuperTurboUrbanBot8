from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *
from databases import Database

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
kb.add(button1)
kb.add(button2)

button11 = KeyboardButton(text='Рассчитать')
button12 = KeyboardButton(text='Информация')
button13 = KeyboardButton(text='Купить')
button14 = KeyboardButton(text="Регистрация")
kb1 = ReplyKeyboardMarkup(resize_keyboard=True).row(button11, button12, button13, button14)


button21 = InlineKeyboardButton(text='Produkt1', callback_data='product_buying')
button22 = InlineKeyboardButton(text='Produkt2', callback_data='product_buying')
button23 = InlineKeyboardButton(text='Produkt3', callback_data='product_buying')
button24 = InlineKeyboardButton(text='Produkt4', callback_data='product_buying')
kb_prod = InlineKeyboardMarkup().row(button21, button22, button23, button24)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

@dp.message_handler(text='Регистрация')
async def sing_up(message, state):
    await message.answer('Введите имя пользователя (только латинский алфавит):', reply_markup=kb1)
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(first= message.text)
    data = await state.get_data()
    if not is_included(data['first']):
        RegistrationState.username = data['first']
        await message.answer('Введите свой email:', reply_markup=kb1)
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя.', reply_markup=kb1)
        await sing_up(message)


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(two= message.text)
    RegistrationState.email = message.text
    await message.answer('Введите свой возраст:', reply_markup=kb1)
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(three= message.text)
    RegistrationState.age = message.text
    data = await state.get_data()
    add_user(data['first'], data['two'], data['three'])
    await message.answer('Удачная регистрация', reply_markup=kb1)
    await state.finish()



@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    await message.answer(get_all_produkts()[1])
    with open('files/753603.png', 'rb') as img1:
        await message.answer_photo(img1)
    await message.answer(get_all_produkts()[2])
    with open('files/6008126.png', 'rb') as img2:
        await message.answer_photo(img2)
    await message.answer(get_all_produkts()[3])
    with open('files/4319549.png', 'rb') as img3:
        await message.answer_photo(img3)
    await message.answer(get_all_produkts()[4])
    with open('files/1044134.png', 'rb') as img4:
        await message.answer_photo(img4)
    await message.answer('Выберите продукт для покупки', reply_markup=kb_prod)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт')
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью', reply_markup=kb1)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(two=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(three=message.text)
    data = await state.get_data()
    for k, v in data.items():
        data[k] = int(v)
    c = 10 * data['three'] + 6.25 * data['two'] - 5 * data['first'] + 5
    await message.answer(f'Ваша норма калорий {c}', reply_markup=kb1)
    await state.finish()


@dp.message_handler()
async def all_message(message):
    #print('Введите команду /start чтобы начать общение.')
    await message.answer('Введите команду /start чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
