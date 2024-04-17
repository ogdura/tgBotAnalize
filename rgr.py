import asyncio
from aiogram import Bot, Dispatcher
from config.config import token
from handlers import user_commands
async def main():
    bot = Bot(token)
    dp = Dispatcher()

    dp.include_router(user_commands.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
