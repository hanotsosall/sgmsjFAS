from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import Command
from ...config import config

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    # Создаём пользователя в БД, если нет
    from ...database import SessionLocal
    from ...models import User
    db = SessionLocal()
    user = db.query(User).filter(User.tg_id == user_id).first()
    if not user:
        user = User(tg_id=user_id, energy=30, gems=0)
        db.add(user)
        db.commit()
    db.close()

    text = (
        "✨ <b>Veluna</b> — твой мир аниме-персонажей с ИИ.\n\n"
        "🎭 Общайся в ролевых играх\n"
        "🎨 Генерируй арты через OOC-команды\n"
        "💎 Покупай гемы за Telegram Stars\n\n"
        "👇 Нажми кнопку, чтобы открыть приложение"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Открыть Veluna", web_app=WebAppInfo(url=config.WEBAPP_URL))],
        [InlineKeyboardButton(text="📢 Наш канал", url="https://t.me/veluna_channel")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ])
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "help")
async def help_callback(callback):
    await callback.message.edit_text(
        "📖 <b>Как играть:</b>\n\n"
        "• Выбери персонажа в Mini App\n"
        "• Начни диалог — расходуется ⚡ Энергия\n"
        "• Пиши <code>(OOC) промт</code> или <code>!img промт</code> для генерации картинки (5 💎)\n"
        "• Пополняй баланс через Telegram Stars\n\n"
        "❓ Если AI выходит из роли, напиши OOC: стоп"
    )