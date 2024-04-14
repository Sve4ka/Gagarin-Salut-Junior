from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("Авторизоваться", callback_data="start")
    keyboard.add(button)
    return keyboard


def login_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("E-mail", callback_data="email")
    button2 = InlineKeyboardButton("Пароль", callback_data="pass")
    kb.add(button).add(button2)
    return kb


def ret_login_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("cancel", callback_data="ret_login")
    kb.add(button)
    return kb


def q_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("Вопросы", callback_data="question")
    kb.add(button)
    return kb


def epi_and_bio() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("Эпитафии", callback_data="epi")
    kb.add(button)
    button = InlineKeyboardButton("Биографии", callback_data="bio")
    kb.add(button)
    return kb


def epi() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("Новая Эпитафия", callback_data="epi")
    kb.add(button)
    button = InlineKeyboardButton("Использовать эту", callback_data="epi_and_bio")
    kb.add(button)
    return kb


def bio() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("Новая биография", callback_data="bio")
    kb.add(button)
    button = InlineKeyboardButton("Использовать эту", callback_data="epi_and_bio")
    kb.add(button)
    return kb


def ret_prof_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("cancel", callback_data="ret_prof")
    kb.add(button)
    return kb


def profile() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("Рандомная страница", url="https://memorycode.ru/page/35984242")
    for i in range(2):
        b = InlineKeyboardButton("Страница " + str(i + 1), callback_data="profile_" + str(i))
        kb.add(b)
    kb.add(button)
    return kb


def creat_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    b1 = InlineKeyboardButton(text="Имя", callback_data="name_cr")
    b2 = InlineKeyboardButton(text="Фамилия", callback_data="surname_cr")
    b3 = InlineKeyboardButton(text="Отчество", callback_data="fathname_cr")
    b4 = InlineKeyboardButton(text="Дата рождения", callback_data="birth_cr")
    b5 = InlineKeyboardButton(text="Дата смерти", callback_data="dead_cr")
    b4 = InlineKeyboardButton(text="Место рождения", callback_data="birth_p_cr")
    b5 = InlineKeyboardButton(text="Место смерти", callback_data="dead_p_cr")
    b6 = InlineKeyboardButton(text="Фото", callback_data="photo_cr")
    button = InlineKeyboardButton("Cancel", callback_data="ret_start")
    kb.add(b2).add(b1).add(b3).add(b4).add(b5).add(b6).add(button)
    return kb


def question() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = InlineKeyboardButton("Следующая", callback_data="next_q")
    button2 = InlineKeyboardButton("Предыдущая", callback_data="prev_q")
    kb.add(button2, button1)
    return kb


def que1() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    b1 = InlineKeyboardButton(text="Дети", callback_data="child_k")
    b2 = InlineKeyboardButton(text="Супруг/а", callback_data="marry_k")
    b3 = InlineKeyboardButton(text="Гражданство", callback_data="home_k")
    kb.add(b1).add(b2).add(b3)
    return kb


def question_2() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = InlineKeyboardButton("Следующая", callback_data="next_q")
    button2 = InlineKeyboardButton("Предыдущая", callback_data="prev_q")
    button3 = InlineKeyboardButton("Конец", callback_data="finish_q")
    kb.add(button2, button1).add(button3)
    return kb
