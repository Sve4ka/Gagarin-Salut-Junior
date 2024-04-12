from random import choice
from time import time
from aiogram import executor, types
from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types
from config import TOKEN_API
import yagpt.gpt
from yagpt.gpt import epi

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def on_startup(_):
    print("HI, i work")

@dp.message_handler()
async def echo_upper(message: types.Message):
    await message.reply(epi(message.text))


if __name__ == '__main__':
    print('hello world')
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)