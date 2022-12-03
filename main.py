import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
API_TOKEN = os.environ.get("API_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm AndanteBot!\nPowered by aiogram.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)