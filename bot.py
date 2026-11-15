import asyncio, logging, os, aiosqlite
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web

TOKEN = "9000565248:AAEVywBm2ry9tYulkiqhQF-FF2q5060XCvU" 
WEBAPP_URL = "https://твой-домен.up.railway.app" 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def start(m: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть в Казино", web_app=WebAppInfo(url=WEBAPP_URL))]
    ])
    await m.answer(
        f"🎰 <b>LUCKY BEAR</b>\n\nПривет, {m.from_user.first_name}!\n💰 Твой баланс: <b>5000₽</b>\n\nНажми кнопку ниже, чтобы открыть игры:",
        reply_markup=kb, parse_mode="HTML"
    )

async def handle_webapp(request):
    return web.FileResponse('./webapp.html')

async def main():
    app = web.Application()
    app.router.add_get('/', handle_webapp)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    await site.start()
    
    print("Бот и сайт запущены!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
