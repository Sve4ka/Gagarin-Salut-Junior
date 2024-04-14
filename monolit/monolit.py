from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import httpx
import text
from config import TOKEN_API
from db.db import search_id_user
from db import db

import yagpt.gpt

from api.endpoints import LoginData, get_access_token
from db.db import add_user, add_db

from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from db.db import add_deader, free_deader_id
from keyboard import creat_kb as kb

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())


async def get_ps_pages(tg_id):
    token = db.answer_bd("select token from user_table where tg_id = %s", tg_id)[0]
    url = "https://mc.dev.rand.agency/api/v1/get-access-token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": token
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            return 'error'
    return response.json()


class Api_State:
    name = State()
    surname = State()
    patronym = State()
    birthday_at = State()
    died_at = State()
    epitaph = State()
    author_epitaph = State()
    video_links = State()
    external_links = State()
    published_page = State()
    accessible_by_password = State()
    access_password = State()
    user_id = State()
    master_id = State()
    page_type_id = State()
    created_at = State()
    updated_at = State()
    deleted_at = State()
    slug = State()
    burial_id = State()
    price = State()
    commission = State()
    video_images = State()
    payment_id = State()
    blank_id = State()
    is_blank = State()
    is_vip = State()
    views = State()
    visitors = State()
    lead_id = State()
    index_page = State()
    filled_fields = State()
    position = State()
    is_referral = State()
    banner_enabled = State()
    locale = State()
    was_indexed = State()
    qr_hidden = State()
    historical_status_id = State()
    count_filled_fields = State()
    parent_tree_id = State()
    custom_birthday_at = State()
    custom_died_at = State()
    main_image = State()
    start = State()
    end = State()
    lastName = State()
    firstName = State()
    link = State()
    free_access = State()
    full_name = State()
    burial_place = State()
    page_type_name = State()
    count_fields = State()
    media = State()


class LoginState(StatesGroup):
    email = State()
    parow = State()
    wait = State()

async def creat_memory(pp, state: FSMContext):
    await state.update_data(id=pp["id"])
    await state.update_data(name=pp["name"])
    await state.update_data(surname=pp["surname"])
    await state.update_data(patronym=pp["patronym"])
    await state.update_data(birthday_at=pp["birthday_at"])
    await state.update_data(died_at=pp['died_at'])
    await state.update_data(epitaph=pp["epitaph"])
    await state.update_data(author_epitaph=pp["author_epitaph"])
    await state.update_data(video_links=pp["video_links"])
    await state.update_data(external_links=pp["external_links"])
    await state.update_data(published_page=pp["published_page"])
    await state.update_data(accessible_by_password=pp["accessible_by_password"])
    await state.update_data(access_password=pp["access_password"])
    await state.update_data(user_id=pp["user_id"])
    await state.update_data(master_id=pp["master_id"])
    await state.update_data(page_type_name=pp["page_type_name"])
    await state.update_data(created_at=pp["created_at"])
    await state.update_data(updated_at=pp["updated_at"])
    await state.update_data(deleted_at=pp["deleted_at"])
    await state.update_data(slug=pp["slug"])
    await state.update_data(burial_id=pp["burial_id"])
    await state.update_data(price=pp["price"])
    await state.update_data(commission=pp["commission"])
    await state.update_data(video_images=pp["video_images"])
    await state.update_data(payment_id=pp["payment_id"])
    await state.update_data(blank_id=pp["blank_id"])
    await state.update_data(is_blank=pp["is_blank"])
    await state.update_data(is_vip=pp["is_vip"])
    await state.update_data(views=pp["views"])
    await state.update_data(visitors=pp["visitors"])
    await state.update_data(lead_id=pp["lead_id"])
    await state.update_data(index_page=pp["index_page"])
    await state.update_data(filled_fields=pp["filled_fields"])
    await state.update_data(position=pp["position"])
    await state.update_data(is_referral=pp["is_referral"])
    await state.update_data(banner_enabled=pp["banner_enabled"])
    await state.update_data(locale=pp["locale"])
    await state.update_data(was_indexed=pp["was_indexed"])
    await state.update_data(qr_hidden=pp["qr_hidden"])
    await state.update_data(historical_status_id=pp["historical_status_id"])
    await state.update_data(count_filled_fields=pp["count_filled_fields"])
    await state.update_data(parent_tree_id=pp["parent_tree_id"])
    await state.update_data(custom_birthday_at=pp["custom_birthday_at"])
    await state.update_data(custom_died_at=pp["custom_died_at"])
    await state.update_data(main_image=pp["main_image"])
    await state.update_data(start=pp["start"])
    await state.update_data(end=pp["end"])
    await state.update_data(last_name=pp["last_name"])
    await state.update_data(first_name=pp["first_name"])
    await state.update_data(link=pp["link"])
    await state.update_data(free_access=pp["free_access"])
    await state.update_data(full_name=pp["full_name"])
    await state.update_data(burial_place=pp["burial_place"])
    await state.update_data(page_type_name=pp["page_type_name"])
    await state.update_data(count_fields=pp["count_fields"])
    await state.update_data(media=pp["media"])


def data_api(tg_ip, state):
    pp = get_ps_pages(tg_ip)
    if pp != "error":
        creat_memory(pp, state)


#   начало работы
@dp.message_handler(commands=['start'], state="*")
async def command_start(message: types.Message, state: FSMContext):
    await message.answer(text=text.START, parse_mode='HTML')
    if search_id_user(message.from_user.id) == 0:
        await message.answer(text=text.START2, reply_markup=kb.start())
    else:
        data_api(message.from_user.id, state)
        await message.answer(text=text.START3, reply_markup=kb.profile(2))
    await message.delete()


#   вход в сайт

DATA = """
ВВЕДИТЕ Ваш email и пароль, по которым вы зарегестрированны на memmorycode
email        {}
Пароль       {}
"""


async def update_keyboard(state: FSMContext):
    async with state.proxy() as data:
        e = data['email']
        parow = data['parow']
        call = data['callback']
        if parow != "None" and e != "None":
            tt = kb.login_kb()
            tt.add(InlineKeyboardButton(text='все верно', callback_data="cr_pr_ok"))
            await call.message.edit_text(text="проверьте введенные данные и если все "
                                              "верно нажмите на соответсвующую кнопку \n\n" +
                                              DATA.format(e, parow),
                                         reply_markup=tt)
        else:
            await call.message.edit_text(DATA.format(e, parow),
                                         reply_markup=kb.login_kb())


@dp.callback_query_handler(text='start', state="*")
async def new_fr(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(email="None")
    await state.update_data(parow="None")
    await state.update_data(callback=call)
    await update_keyboard(state)


@dp.callback_query_handler(text='email', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите вашу почту", reply_markup=kb.ret_login_kb())
    await LoginState.email.set()


@dp.callback_query_handler(text='pass', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("введите ваш пароль", reply_markup=kb.ret_login_kb())
    await LoginState.parow.set()


@dp.callback_query_handler(text='ret_login', state='*')
async def new_cancel(call: types.CallbackQuery, state: FSMContext):
    await update_keyboard(state)
    await LoginState.wait.set()


@dp.callback_query_handler(text='cr_pr_ok', state="*")
async def inl_new_fr_name(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        e = data['email']
        pa = data['parow']
    L = LoginData
    L.email = e
    L.password = pa
    L.device = 'Iphone7'
    add_user(call.message.chat.id, e)
    if await get_access_token(L) == "error":
        await call.message.edit_text(text="неверно введены данные\n" + DATA.format(e, pa),
                                     reply_markup=kb.login_kb())
        add_db("delete from user_table where tg_id=%s", call.message.chat.id)
        await LoginState.wait.set()
        return
    await state.finish()
    data_api(call.message.chat.id, state)
    await call.message.edit_text("Данные сохранены\n\n", reply_markup=kb.profile(2))


@dp.message_handler(state=LoginState.email)
async def price_state(message: types.Message, state: FSMContext):
    em = message.text.lower()
    await state.update_data(email=em)
    await update_keyboard(state)
    await message.delete()
    await state.set_state(LoginState.wait.state)


@dp.message_handler(state=LoginState.parow)
async def price_state(message: types.Message, state: FSMContext):
    em = message.text
    await state.update_data(parow=em)
    await update_keyboard(state)
    await message.delete()
    await state.set_state(LoginState.wait.state)


@dp.message_handler(state=LoginState.wait)
async def wait_state(message: types.Message, state: FSMContext):
    await update_keyboard(state)


#


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


async def update_keyboard_first(state: FSMContext):
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


QQ = ["С кем он был близок", "Расскажите про его профессию", "где он учился",
      "что было важно для него", "чем он увлекался", "Место рождения почившего",
      "Образование", "Место работы", "Место смерти",
      "Характер", "Отношения с близкими", "Любимые хобби", "Яркое воспоминание"]

SIZE = len(QQ)


#  ввод-вывод вопросов
class QuestionState(StatesGroup):
    question = State()
    epi = State()
    bio = State()
    epi_bio = State()
    wait = State()


@dp.callback_query_handler(text='question', state="*")
async def new_fr(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(num=0)
    await state.update_data(question=[i for i in range(SIZE)])
    await state.update_data(answer=[])
    await state.update_data(kb=kb.question())
    await state.update_data(callback=call)
    await call.message.edit_text(QQ[0], reply_markup=kb.question())
    await QuestionState.question.set()


@dp.callback_query_handler(text='next_q', state="*")
async def next_fr(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        num = data['num'] + 1
        qq = data['question']
        kb_ = data['kb']
        if num >= len(qq):
            num = 0
        q = QQ[qq[num]]
        a = data['answer']
    print(a)
    if len(qq) == SIZE - 5:
        kb_ = kb.question_2()
        await state.update_data(kb=kb_)

    await state.update_data(num=num)
    await call.message.edit_text(q, reply_markup=kb_)
    await QuestionState.question.set()


@dp.callback_query_handler(text='prev_q', state="*")
async def next_fr(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        num = data['num'] - 1
        qq = data['question']
        if num < 0:
            num = len(qq) - 1
        q = QQ[qq[num]]
        kb_ = data['kb']
    if len(qq) == SIZE - 5:
        kb_ = kb.question_2()
        await state.update_data(kb=kb_)
    await state.update_data(num=num)
    await call.message.edit_text(q, reply_markup=kb_)
    await QuestionState.question.set()


@dp.callback_query_handler(text='finish_q', state="*")
async def next_fr(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        aa = data['answer']
    await QuestionState.epi_bio.set()
    await epi_bio(state, call.from_user.id)

    await call.message.edit_text("\n".join([" - ".join(i) for i in aa]), reply_markup=kb.epi_and_bio())


@dp.message_handler(state=QuestionState.question)
async def price_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        num = data['num']
        qq = data['question']
        q = QQ[qq[num]]
        a = data['answer']
        call = data['callback']
        kb_ = data['kb']
    if len(qq) == SIZE - 5:
        kb_ = kb.question_2()
        await state.update_data(kb=kb_)
    ph = message.text.lower()
    a.append([q, ph])
    qq = qq[:num] + qq[num + 1:]
    if len(qq) >= num:
        await state.update_data(num=0)
    await state.update_data(answer=a)
    await state.update_data(question=qq)
    await message.delete()
    q = QQ[qq[num]]
    await call.message.edit_text(q, reply_markup=kb_)


#  работа с эпитафиями и био

async def epi_bio(state: FSMContext, id):
    await state.update_data(dead=db.search_id_dead(id))
    await state.update_data(epi="")
    await state.update_data(bio="")


@dp.callback_query_handler(text='epi_and_bio', state="*")
async def next_fr(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        aa = data['answer']
    await QuestionState.epi_bio.set()

    await call.message.edit_text("\n".join([" - ".join(i) for i in aa]), reply_markup=kb.epi_and_bio())


@dp.callback_query_handler(text='epi', state="*")
async def next_fr(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        aa = data['answer']
    fio = db.ret_data_dead(db.search_id_dead(call.message.chat.id))[0]
    tt = "Обработка информации"
    await call.message.edit_text(tt, reply_markup=kb.epi())
    tt = yagpt.gpt.epi("\n".join([" - ".join(i) for i in aa]), fio[2] + " " + fio[3] + " " + fio[4])
    await call.message.edit_text(tt, reply_markup=kb.epi())
    await state.update_data(epi=tt)
    # await call.message.edit_text(q, reply_markup=kb_)
    await QuestionState.question.set()


@dp.callback_query_handler(text='bio', state="*")
async def next_fr(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        aa = data['answer']
    fio = db.ret_data_dead(db.search_id_dead(call.message.chat.id))[0]
    tt = "Обработка информации"
    await call.message.edit_text(tt, reply_markup=kb.bio())
    tt = yagpt.gpt.bio("\n".join([" - ".join(i) for i in aa]), fio[2] + " " + fio[3] + " " + fio[4])
    await call.message.edit_text(tt, reply_markup=kb.bio())
    await state.update_data(bio=tt)
    # await call.message.edit_text(q, reply_markup=kb_)
    await QuestionState.question.set()
