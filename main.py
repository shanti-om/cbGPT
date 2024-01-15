import asyncio
import logging
from bot import tbot


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


async def main():
    # Запуск процесса поллинга новых апдейтов
    async def main_bot():
        print('started')
        # await dp.start_polling(bot)   # Запуск бота без параметров
        await tbot.bot.delete_webhook()
        await tbot.dp.start_polling(tbot.bot, mylist=[1, 2, 3])   # Передача параметров в бота через параметры (именованые kwargs)

    async def msg_queue():
        pass

    await asyncio.gather(main_bot(), msg_queue())


if __name__ == "__main__":
    asyncio.run(main())
