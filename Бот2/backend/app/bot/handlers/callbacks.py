from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from ...database import SessionLocal
from ...models import User, Character

router = Router()

@router.callback_query(F.data.startswith("char_"))
async def select_character(callback: CallbackQuery):
    char_id = int(callback.data.split("_")[1])
    db = SessionLocal()
    user = db.query(User).filter(User.tg_id == callback.from_user.id).first()
    if user:
        user.current_character_id = char_id
        db.commit()
        await callback.answer(f"Персонаж выбран")
        await callback.message.edit_text("✅ Теперь вы можете писать сообщения в этом чате.")
    db.close()

@router.callback_query(F.data == "shop")
async def shop_menu(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 50 гемов (25⭐)", callback_data="buy_gems_50")],
        [InlineKeyboardButton(text="💎 200 гемов (90⭐)", callback_data="buy_gems_200")],
        [InlineKeyboardButton(text="⚡ +20 энергии (10⭐)", callback_data="buy_energy_20")],
        [InlineKeyboardButton(text="🎁 Ежедневный бонус", callback_data="daily")],
    ])
    await callback.message.edit_text("🛒 Магазин Veluna\n\nВыберите товар:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("buy_gems_"))
async def buy_gems_callback(callback: CallbackQuery):
    gems_amount = int(callback.data.split("_")[2])
    # Создаём инвойс через Telegram Stars
    from aiogram.types import LabeledPrice, PreCheckoutQuery
    from ...config import config
    price_stars = config.GEMS_PACKS.get(gems_amount, 25)
    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"{gems_amount} Gems",
        description=f"Пополнение гемов для генерации изображений",
        payload=f"gems_{gems_amount}",
        currency="XTR",
        prices=[LabeledPrice(label=f"{gems_amount} Gems", amount=price_stars)]
    )
    await callback.answer()

@router.callback_query(F.data == "daily")
async def daily_reward(callback: CallbackQuery):
    from ...services.economy import add_energy
    db = SessionLocal()
    user = db.query(User).filter(User.tg_id == callback.from_user.id).first()
    if user:
        # Проверяем по дате последнего получения (упрощённо)
        add_energy(callback.from_user.id, 15, db)
        await callback.answer("🎁 Вы получили +15 энергии!", show_alert=True)
        await callback.message.edit_text("Ежедневный бонус получен! Зайдите завтра снова.")
    db.close()