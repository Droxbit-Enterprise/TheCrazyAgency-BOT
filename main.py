from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from handlers.start import start_router
from handlers.menu import menu_router
from handlers.register import register_router
# from apps.sugo import sugo_router
# from apps.contigo import contigo_router
# from apps.meyo import meyo_router
# from apps.salsa import salsa_router
# from apps.timo import timo_router
# from apps.kito import kito_router
from database import init_db

async def main():
    init_db()
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(register_router)
    # dp.include_router(sugo_router)
    # dp.include_router(contigo_router)
    # dp.include_router(meyo_router)
    # dp.include_router(salsa_router)
    # dp.include_router(timo_router)
    # dp.include_router(kito_router)
    print("🔥 El bot de The Crazy Agency está corriendo correctamente... 💎")

    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())