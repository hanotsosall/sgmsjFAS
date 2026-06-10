from aiogram import Router, F
from aiogram.types import Message
from ...database import SessionLocal
from ...models import User

router = Router()

@router.message(F.text.lower() == "ooc off")
async def ooc_off(message: Message):
    db = SessionLocal()
    user = db.query(User).filter(User.tg_id == message.from_user.id).first()
    if user:
        user.ooc_mode = False
        db.commit()
        await message.answer("[Система] Режим OOC выключен. Возвращаемся в роль.")
    db.close()