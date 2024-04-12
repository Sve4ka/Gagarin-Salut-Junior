#  здесь описывается реакция на различные команды + генерируется сам бот

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())


