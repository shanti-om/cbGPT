#from cfg_reader import config
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, URLInputFile, BufferedInputFile
from aiogram.filters import Command, CommandObject
from datetime import datetime
import g4f


class Tbot:
    BOT_TOKEN = '6952712860:AAHHXFN6KF_odEiiMT_frHMP__Z1eXFbklk'
    in_work = 0
    filter_rating = 4
    filter_feedbacks = 1600
    emp_cat = 0
    no_img = 0
    done = 0
    bot_started_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def __init__(self):
        self.dp = Dispatcher()
        self.bot = Bot(token=Tbot.BOT_TOKEN, parse_mode='HTML')
        # Словарь для хранения истории разговоров
        self.conversation_history = {}

    def trim_history(self, history, max_length=4096):
        current_length = sum(len(message["content"]) for message in history)
        while history and current_length > max_length:
            removed_message = history.pop(0)
            current_length -= len(removed_message["content"])
        return history


tbot = Tbot()


# Хэндлер на команду /start
@tbot.dp.message(Command("start"))
async def cmd_start(message: types.Message):

    if not Tbot.in_work:
        Tbot.in_work = 1
        # await tbot.cycle()
        await message.answer("Bot started")
    else:
        await message.answer("Bot already in progress...")

# Хэндлер на команду /start
@tbot.dp.message(Command("srt"))
async def cmd_srt(message: types.Message):

    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        messages=[{'content': 'HI'}],
        provider=g4f.Provider.GeekGpt,
    )
    chat_gpt_response = response

    await message.answer(chat_gpt_response)

# Обработчик для каждого нового сообщения


@tbot.dp.message()
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_input = message.text

    if user_id not in tbot.conversation_history:
        tbot.conversation_history[user_id] = []

    tbot.conversation_history[user_id].append({"role": "user", "content": user_input})
    tbot.conversation_history[user_id] = tbot.trim_history(tbot.conversation_history[user_id])

    chat_history = tbot.conversation_history[user_id]

    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=chat_history,
            provider=g4f.Provider.Bing,
        )
        chat_gpt_response = response
    except Exception as e:
        print(f"{g4f.Provider.GeekGpt.__name__}:", e)
        chat_gpt_response = "Извините, произошла ошибка."

    tbot.conversation_history[user_id].append({"role": "assistant", "content": chat_gpt_response})
    print(tbot.conversation_history)
    length = sum(len(message["content"]) for message in tbot.conversation_history[user_id])
    print(length)
    await message.answer(chat_gpt_response)
