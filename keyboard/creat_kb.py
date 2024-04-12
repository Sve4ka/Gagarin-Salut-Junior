from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("авторизоваться", callback_data="start")
    keyboard.add(button)
    return keyboard


def login_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("email", callback_data="email")
    button1 = InlineKeyboardButton("phone", callback_data="phone")
    kb.add(button).add(button1)
    return kb

def ret_login_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("cancel", callback_data="ret_login")
    kb.add(button)
    return kb


def ret_prof_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("cancel", callback_data="ret_prof")
    kb.add(button)
    return kb

def profile()-> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = InlineKeyboardButton("рандомная страничка", url= "https://memorycode.ru/page/35984242")
    button1 = InlineKeyboardButton("Создать свою страничку", callback_data="profile")
    kb.add(button).add(button1)
    return kb

def creat_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    b1 = InlineKeyboardButton(text="имя", callback_data="name_cr")
    b2 = InlineKeyboardButton(text="фамилия", callback_data="surname_cr")
    b3 = InlineKeyboardButton(text="отчество", callback_data="fathname_cr")
    b4 = InlineKeyboardButton(text="дата рождения", callback_data="birth_cr")
    b5 = InlineKeyboardButton(text="дата смерти", callback_data="dead_cr")
    kb.add(b1).add(b2).add(b3).add(b4).add(b5)
    return kb