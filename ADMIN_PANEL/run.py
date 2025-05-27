import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher


from app.handlers.admin import router as admin_router
from app.handlers.user import router as user_router




async def main():
    load_dotenv()
    dp = Dispatcher()
    bot = Bot(token=os.getenv("TG_TOKEN"))
    
    dp.register_startup(startup)
    dp.register_shutdown(shutdown)
    
    dp.include_routers(admin_router, user_router)
    await dp.start_polling(bot)
    
    
async def startup(dp: Dispatcher):
    print("Bot is starting...")
    
    
async def shutdown(dp: Dispatcher):
    print("Bot is stopping...")
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")