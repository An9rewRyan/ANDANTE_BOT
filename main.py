from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from dotenv import load_dotenv
import os
from aiogram.fsm.context import FSMContext
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from youtube import out
from aiogram.types.input_file import URLInputFile
import sys
import asyncio
import logging
from aiogram.filters import Command
from aiogram.types import FSInputFile

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
API_TOKEN = os.environ.get("API_TOKEN")
CHANNEL_NAME = os.environ.get("CHANNEL_NAME")
test_message = "Hello bitchessssss!"

bot = Bot(API_TOKEN, parse_mode="HTML")
form_router = Router()


class States(StatesGroup):
    main = State()
    track = State()

@form_router.message(Command(commands=["title"]))
async def track_name(message: Message, state: FSMContext, dialog_manager: DialogManager|None = None, ):
    await state.set_state(States.track)
    await message.reply("Введите название трека: ")

@form_router.message(States.track)
async def send_message(message: Message, state: FSMContext):
    track_name, artist = out(message.text)
    print(os.path.join(BASE_DIR, f'{artist} - {track_name}.mp3'))
    file = FSInputFile(path = os.path.join(BASE_DIR, f'{artist} - {track_name}.mp3'))
    await bot.send_audio(message.chat.id, file, performer = artist, title = track_name)
    os.remove(os.path.join(BASE_DIR, f'{artist} - {track_name}.mp3'))

main_window = Window(
    Const("Меню"),
    Button(Const("Найти трек по названию"), id="sender", on_click=track_name),
    state=States.main,
)

@form_router.message(Command(commands=["start"]))
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(States.main, mode=StartMode.RESET_STACK)

async def main():
    dp = Dispatcher()
    dp.include_router(form_router)
    storage = MemoryStorage()
    registry = DialogRegistry(dp)
    dialog = Dialog(main_window)
    registry.register(dialog)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

