from datetime import datetime
from pprint import pprint
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton

from command import dp, bot
from db.db import add_deader, free_deader_id
from keyboard import creat_kb as kb

DATA_CR = """
Введите данные человека
Фамилия        = {}
Имя            = {}
Отчество       = {}
Дата рождения  = {}
Дата смерти    = {}
Место рождения = {}
Место смерти   = {}
"""


class CreatState(StatesGroup):
    name = State()
    surname = State()
    fathname = State()
    birth = State()
    dead = State()
    birth_place = State()
    death_place = State()
    wait = State()
    photo = State()


async def update_keyboard(state: FSMContext):
    async with state.proxy() as data:
        n = data['name']
        s = data['surname']
        f = data['fathname']
        b = data['birth']
        d = data['dead']
        pb = data['birth_place']
        pd = data['death_place']
        p = data['photo']
        call = data['callback']
        if sum([1 if i != "None" else 0 for i in [n, s, f, b, d, p, pb, pd]]) == 8:
            tt = kb.creat_kb()
            tt.add(InlineKeyboardButton(text='все верно', callback_data="pr_ok"))
            await call.message.edit_text(text="проверьте введенные данные и если все "
                                              "верно нажмите на соответсвующую кнопку \n\n" +
                                              DATA_CR.format(s, n, f, b, d, pb, pd),
                                         reply_markup=tt)
        else:
            if b == "None":
                b = "xx/xx/xxxx"
            if d == "None":
                d = "xx/xx/xxxx"
            await call.message.edit_text(DATA_CR.format(s, n, f, b, d, pb, pd), reply_markup=kb.creat_kb())


@dp.callback_query_handler(text='profile', state="*")
async def new_fr(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(name="None")
    await state.update_data(surname="None")
    await state.update_data(fathname="None")
    await state.update_data(birth="None")
    await state.update_data(dead="None")
    await state.update_data(birthp="None")
    await state.update_data(deadp="None")

    await state.update_data(photo="None")
    await state.update_data(ph_call="None")
    await state.update_data(callback=call)
    await update_keyboard(state)


@dp.callback_query_handler(text='name_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите имя", reply_markup=kb.ret_prof_kb())
    await CreatState.name.set()


@dp.callback_query_handler(text='photo_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Отправьте фото", reply_markup=kb.ret_prof_kb())
    await CreatState.photo.set()


@dp.callback_query_handler(text='surname_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите фамилию", reply_markup=kb.ret_prof_kb())
    await CreatState.surname.set()


@dp.callback_query_handler(text='fathname_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите отчество, при остутсвии введите -", reply_markup=kb.ret_prof_kb())
    await CreatState.fathname.set()


@dp.callback_query_handler(text='birth_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите дату рождения, в формате дд/мм/гггг", reply_markup=kb.ret_prof_kb())
    await CreatState.birth.set()


@dp.callback_query_handler(text='dead_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите дату смерти, в формате дд/мм/гггг", reply_markup=kb.ret_prof_kb())
    await CreatState.dead.set()


@dp.callback_query_handler(text='birth_pl_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите место рождение", reply_markup=kb.ret_prof_kb())
    await CreatState.birth.set()


@dp.callback_query_handler(text='dead_pl_cr', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите место смерти", reply_markup=kb.ret_prof_kb())
    await CreatState.dead.set()


@dp.callback_query_handler(text='ret_prof', state='*')
async def new_cancel(call: types.CallbackQuery, state: FSMContext):
    await update_keyboard(state)
    await CreatState.wait.set()


@dp.callback_query_handler(text='ret_start', state='*')
async def new_cancel(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        p = data['ph_call']
    await state.finish()
    if p != "None":
        await p.delete()
    await call.message.edit_text("Главное меню", reply_markup=kb.profile())


@dp.callback_query_handler(text='pr_ok', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        n = data['name']
        s = data['surname']
        f = data['fathname']
        b = data['birth']
        d = data['dead']
        photo = data['photo']
        p = data['ph_call']

    b = datetime.strptime(b, '%d/%m/%Y').date()
    d = datetime.strptime(d, '%d/%m/%Y').date()
    await state.finish()
    await p.delete()
    add_deader(call.message.chat.id, n, s, f, b, d, photo)
    await call.message.edit_text("Данные сохранены\n\n перейдем в создание эпитафии и биографии, "
                                 "для этого вам необходимо ответить хотябы на 5 вопросов",
                                 reply_markup=kb.q_kb())


@dp.message_handler(state=CreatState.name)
async def price_state(message: types.Message, state: FSMContext):
    ph = message.text.lower()
    await state.update_data(name=ph.capitalize())
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)


@dp.message_handler(state=CreatState.surname)
async def price_state(message: types.Message, state: FSMContext):
    ph = message.text.lower()
    await state.update_data(surname=ph.capitalize())
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)


@dp.message_handler(state=CreatState.fathname)
async def price_state(message: types.Message, state: FSMContext):
    ph = message.text.lower()
    await state.update_data(fathname=ph.capitalize())
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)


@dp.message_handler(state=CreatState.birth)
async def price_state(message: types.Message, state: FSMContext):
    date = message.text.lower()
    try:
        valid_date = datetime.strptime(date, '%d/%m/%Y')
    except:
        await message.delete()
        return
    get_date = lambda d: datetime.strptime(d, '%d.%m.%Y').date() <= datetime.today().date()
    if not get_date(date):
        await message.delete()
        return
    await state.update_data(birth=date)
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)


@dp.message_handler(state=CreatState.dead)
async def price_state(message: types.Message, state: FSMContext):
    date = message.text.lower()
    try:
        valid_date = datetime.strptime(date, '%d/%m/%Y')
    except:
        await message.delete()
        return
    get_date = lambda d: datetime.strptime(d, '%d.%m.%Y').date() <= datetime.today().date()
    await state.update_data(dead=date)
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)


@dp.message_handler(state=CreatState.photo, content_types=types.ContentType.PHOTO)
async def price_state(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file="./photo/" + str(free_deader_id()) + '.jpg')
    ph_call = await bot.send_photo(message.chat.id, message.photo[-1].file_id)
    await state.update_data(ph_call=ph_call)
    await state.update_data(photo="./photo/" + str(free_deader_id()) + '.jpg')
    await update_keyboard(state)
    await message.delete()
    await state.set_state(CreatState.wait.state)


@dp.message_handler(state=CreatState.photo)
async def price_state(message: types.Message, state: FSMContext):
    await message.delete()


@dp.message_handler(state=CreatState.wait)
async def wait_state(message: types.Message, state: FSMContext):
    await update_keyboard(state)
