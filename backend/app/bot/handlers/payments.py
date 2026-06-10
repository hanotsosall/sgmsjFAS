from aiogram import Router, F
from aiogram.types import PreCheckoutQuery, Message, SuccessfulPayment
from ...database import SessionLocal
from ...models import User, Purchase
from ...services.economy import add_gems, add_energy

router = Router()

@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    stars_amount = message.successful_payment.total_amount  // 100  # XTR: 1 Star = 100
    db = SessionLocal()
    user = db.query(User).filter(User.tg_id == message.from_user.id).first()
    if not user:
        db.close()
        await message.answer("Ошибка: пользователь не найден.")
        return
    if payload.startswith("gems_"):
        gems = int(payload.split("_")[1])
        add_gems(message.from_user.id, gems, db)
        purchase = Purchase(user_id=user.id, stars_amount=stars_amount, gems_received=gems, status="completed")
        db.add(purchase)
        db.commit()
        await message.answer(f"✅ Пополнение успешно! Вы получили {gems} 💎. Баланс: {user.gems} гемов.")
    elif payload.startswith("energy_"):
        energy = int(payload.split("_")[1])
        add_energy(message.from_user.id, energy, db)
        purchase = Purchase(user_id=user.id, stars_amount=stars_amount, energy_received=energy, status="completed")
        db.add(purchase)
        db.commit()
        await message.answer(f"✅ +{energy} ⚡ энергии.")
    db.close()