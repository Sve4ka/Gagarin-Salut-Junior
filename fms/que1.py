from datetime import datetime
from pprint import pprint
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton

from command import dp, bot
from db.db import add_deader, add_db
from keyboard import creat_kb as kb

DATA_CR = """
введите данные человека
Дети            = {}
Супруг/а        = {}
Гражданство     = {}
"""


class Q1State(StatesGroup):
    child = State()
    marry = State()
    home = State()
    wait = State()


async def update_keyboard_1(state: FSMContext):
    async with state.proxy() as data:
        c = data["child"]
        m = data["marry"]
        h = data["home"]
        call = data['callback']
        if sum([1 if i != "None" else 0 for i in [c, m, h]]) == 3:
            tt = kb.creat_kb()
            tt.add(InlineKeyboardButton(text='Все верно', callback_data="pr1_ok"))
            await call.message.edit_text(text="Проверьте введенные данные и, если все "
                                              "верно, нажмите на соответсвующую кнопку \n\n" +
                                              DATA_CR.format(c, m, h),
                                         reply_markup=tt)
        else:
            await call.message.edit_text(DATA_CR.format(c, m, h), reply_markup=kb.que1())




@dp.callback_query_handler(text='child_k', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите имена детей")
    await Q1State.child.set()


@dp.callback_query_handler(text='marry_k', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите имя супруга/и")
    await Q1State.marry.set()


@dp.callback_query_handler(text='home_k', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите Гражданство")
    await Q1State.home.set()


@dp.callback_query_handler(text='pr1_ok', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        c = data["child"]
        m = data["marry"]
        h = data["home"]
    await state.finish()
    add_db("insert into dead_table (child, marry, home) values (%s, %s, %s)", c, m, h)
    await call.message.edit_text("Данные сохранены\n\n ",
                                 reply_markup=kb.q2_kb())


@dp.message_handler(state=Q1State.child)
async def price_state(message: types.Message, state: FSMContext):
    ph = message.text
    await state.update_data(child=ph)
    await update_keyboard_1(state)
    await message.delete()
    await state.set_state(Q1State.wait.state)


@dp.message_handler(state=Q1State.marry)
async def price_state(message: types.Message, state: FSMContext):
    ph = message.text
    await state.update_data(marry=ph)
    await update_keyboard_1(state)
    await message.delete()
    await state.set_state(Q1State.wait.state)


@dp.message_handler(state=Q1State.home)
async def price_state(message: types.Message, state: FSMContext):
    ph = message.text
    await state.update_data(home=ph)
    await update_keyboard_1(state)
    await message.delete()
    await state.set_state(Q1State.wait.state)


@dp.message_handler(state=Q1State.wait)
async def wait_state(message: types.Message, state: FSMContext):
    await update_keyboard_1(state)
