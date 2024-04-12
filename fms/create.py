from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from command import dp
from keyboard import creat_kb as kb
from db.db import add_deader

DATA_CR = """
введите данные человека
Фамилия        = {}
Имя            = {}
Отчество       = {}
Дата рождения  = {}
Дата смерти    = {}
"""


class CreatState(StatesGroup):
    name = State()
    surname = State()
    fathname = State()
    birth = State()
    dead = State()
    wait = State()


async def update_keyboard(state: FSMContext):
    async with state.proxy() as data:
        n = data['name']
        s = data['surname']
        f = data['fathname']
        b = data['birth']
        d = data['dead']
        call = data['callback']
        if sum([1 if i != "None" else 0 for i in [n, s, f, b, d]]) == 5:
            tt = kb.creat_kb()
            tt.add(InlineKeyboardButton(text='все верно', callback_data="pr_ok"))
            await call.message.edit_text(text="проверьте введенные данные и если все "
                                              "верно нажмите на соответсвующую кнопку \n\n" +
                                              DATA_CR.format(n, s, f, b, d),
                                         reply_markup=tt)
        else:
            await call.message.edit_text(DATA_CR.format(n, s, f, b, d), reply_markup=kb.creat_kb())


@dp.callback_query_handler(text='profile', state="*")
async def new_fr(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(name="None")
    await state.update_data(surname="None")
    await state.update_data(fathname="None")
    await state.update_data(birth="None")
    await state.update_data(dead="None")
    await state.update_data(callback=call)
    await update_keyboard(state)


@dp.callback_query_handler(text='name_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите имя", reply_markup=kb.ret_prof_kb())
    await CreatState.name.set()


@dp.callback_query_handler(text='surname_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите фамилию", reply_markup=kb.ret_prof_kb())
    await CreatState.surname.set()


@dp.callback_query_handler(text='fathname_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите отчество", reply_markup=kb.ret_prof_kb())
    await CreatState.fathname.set()


@dp.callback_query_handler(text='birth_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите рождение", reply_markup=kb.ret_prof_kb())
    await CreatState.birth.set()


@dp.callback_query_handler(text='dead_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите смерти", reply_markup=kb.ret_prof_kb())
    await CreatState.dead.set()


@dp.callback_query_handler(text='ret_prof', state='*')
async def new_cancel(call: types.CallbackQuery, state: FSMContext):
    await update_keyboard(state)
    await CreatState.wait.set()


@dp.callback_query_handler(text='pr_ok', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        n = data['name']
        s = data['surname']
        f = data['fathname']
        b = data['birth']
        d = data['dead']
    await state.finish()
    add_deader(call.message.chat.id, n, s, f, b, d)
    await call.message.edit_text("Данные сохранены\n\n")


@dp.message_handler(state=CreatState.name)
async def price_state(message: types.Message, state: FSMContext):
    ph = message.text.lower()
    await state.update_data(name=ph)
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)


@dp.message_handler(state=CreatState.surname)
async def price_state(message: types.Message, state: FSMContext):
    ph = message.text.lower()
    await state.update_data(surname=ph)
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)


@dp.message_handler(state=CreatState.fathname)
async def price_state(message: types.Message, state: FSMContext):
    ph = message.text.lower()
    await state.update_data(fathname=ph)
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)



@dp.message_handler(state=CreatState.birth)
async def price_state(message: types.Message, state: FSMContext):
    ph = message.text.lower()
    await state.update_data(birth=ph)
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)


@dp.message_handler(state=CreatState.dead)
async def price_state(message: types.Message, state: FSMContext):
    em = message.text.lower()
    await state.update_data(dead=em)
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)


@dp.message_handler(state=CreatState.wait)
async def wait_state(message: types.Message, state: FSMContext):
    await update_keyboard(state)
