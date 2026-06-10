from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from ..config import config
import logging

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

async def set_webhook():
    await bot.set_webhook(f"{config.WEBHOOK_URL}/webhook")

async def on_startup():
    from .handlers import start, messages, callbacks, payments, ooc
    dp.include_router(start.router)
    dp.include_router(messages.router)
    dp.include_router(callbacks.router)
    dp.include_router(payments.router)
    dp.include_router(ooc.router)
    await set_webhook()