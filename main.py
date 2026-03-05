import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import router

# .env faylini o'qish
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "BOT_TOKEN_SHU_ERGA_YOZING")

logging.basicConfig(level=logging.INFO)

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "BOT_TOKEN_SHU_ERGA_YOZING":
        logging.error("Iltimos, .env faylining ichiga bot tokenini kiriting!")
        return

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
