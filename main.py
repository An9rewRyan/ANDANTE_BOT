from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from dotenv import load_dotenv
import os

from aiogram.dispatcher import FSMContext
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram.types import CallbackQuery
from youtube import out

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
API_TOKEN = os.environ.get("API_TOKEN")
CHANNEL_NAME = os.environ.get("CHANNEL_NAME")
test_message = "Hello bitchessssss!"

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)


class States(StatesGroup):
    main = State()
    track = State()

async def track_name(c: CallbackQuery, button: Button, manager: DialogManager):
    await States.track.set()
    await c.message.reply("Введите название трека: ")

@dp.message_handler(state=States.track)
async def send_message(message: Message, state: FSMContext):
    track_name = out(message.text)
    await bot.send_audio(message.from_user.id, open(os.path.join(BASE_DIR, track_name), "rb"), performer = "Unknown", title = track_name)
    os.remove(os.path.join(BASE_DIR, track_name))

main_window = Window(
    Const("Вы хотите найти трек?"),
    Button(Const("Да"), id="sender", on_click=track_name),
    state=States.main,
)

@dp.message_handler(commands=["start"])
async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(States.main, mode=StartMode.RESET_STACK)

dialog = Dialog(main_window)
registry.register(dialog)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

