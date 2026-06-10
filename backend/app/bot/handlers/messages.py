import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest
from ...services.ai_client import generate_ai_response
from ...services.economy import get_user_balance, deduct_energy, deduct_gems, add_energy
from ...services.image_generator import generate_image_async
from ...database import SessionLocal
from ...models import User, Chat, Message as DBMessage, Character
from ...config import config

router = Router()

@router.message(F.chat.type == "private")
async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text.strip()
    db = SessionLocal()
    user = db.query(User).filter(User.tg_id == user_id).first()
    if not user:
        await message.answer("Нажми /start, чтобы начать")
        db.close()
        return

    # OOC-команда выхода из роли
    if text.lower().startswith("ooc:") and "стоп" in text.lower():
        user.ooc_mode = True
        db.commit()
        await message.answer("[Система] Режим OOC включён. Я буду отвечать вне роли.")
        db.close()
        return

    # Генерация изображения через !img или (OOC)
    img_match = re.match(r'^(!img|\(OOC\))\s+(.+)', text, re.IGNORECASE)
    if img_match:
        prompt = img_match.group(2).strip()
        if not prompt:
            await message.answer("Укажите промт после команды.\nПример: !img девушка с кошкой, аниме")
            db.close()
            return
        if user.gems < config.GEMS_COST_PER_IMAGE:
            await message.answer(f"❌ Не хватает 💎 Гемов. Нужно {config.GEMS_COST_PER_IMAGE} гемов.\nКупите в магазине /shop")
            db.close()
            return
        # Списываем гемы сразу, но генерация асинхронная
        deduct_gems(user_id, config.GEMS_COST_PER_IMAGE, db)
        # Отправляем "генерирую..."
        status_msg = await message.answer("🎨 Генерирую изображение... (до 10 секунд)")
        # Запускаем фоновую задачу
        from ...workers.generation_tasks import generate_image_task
        generate_image_task.delay(
            prompt=prompt,
            user_id=user_id,
            chat_id=message.chat.id,
            message_id=status_msg.message_id,
            aspect_ratio="1:1"
        )
        db.close()
        return

    # Обычное сообщение — ролевой чат или OOC-режим
    # Определяем активного персонажа (если нет, просим выбрать)
    current_char_id = user.current_character_id
    if not current_char_id:
        await message.answer("Сначала выберите персонажа в Mini App или командой /characters")
        db.close()
        return

    # Проверка энергии
    if user.energy < config.ENERGY_COST_PER_MESSAGE:
        await message.answer("⚡ Не хватает энергии. Пополните в магазине или выполните задания.")
        db.close()
        return

    # Если OOC режим — простой ответ без роли
    if user.ooc_mode:
        from ...services.ai_client import simple_chat
        reply = await simple_chat(text)
        deduct_energy(user_id, config.ENERGY_COST_PER_MESSAGE, db)
        await message.answer(reply)
        # Сохраняем сообщения (опционально)
        db.close()
        return

    # Ролевой режим: получаем ответ от AI с системным промптом персонажа
    chat_record = db.query(Chat).filter(
        Chat.user_id == user.id,
        Chat.character_id == current_char_id
    ).first()
    if not chat_record:
        chat_record = Chat(user_id=user.id, character_id=current_char_id)
        db.add(chat_record)
        db.commit()
        db.refresh(chat_record)

    # Сохраняем сообщение пользователя
    user_msg = DBMessage(chat_id=chat_record.id, role="user", content=text)
    db.add(user_msg)
    db.commit()

    # Вызываем AI
    reply = await generate_ai_response(
        user_id=user.id,
        character_id=current_char_id,
        scenario_id=user.current_scenario_id,
        message_text=text,
        db=db,
        ooc_mode=False
    )
    # Сохраняем ответ AI
    assistant_msg = DBMessage(chat_id=chat_record.id, role="assistant", content=reply)
    db.add(assistant_msg)
    deduct_energy(user_id, config.ENERGY_COST_PER_MESSAGE, db)
    db.commit()
    await message.answer(reply)
    db.close()

@router.message(Command("energy"))
async def cmd_energy(message: Message):
    user_id = message.from_user.id
    db = SessionLocal()
    user = db.query(User).filter(User.tg_id == user_id).first()
    if user:
        await message.answer(f"⚡ Ваша энергия: {user.energy}\n💎 Гемы: {user.gems}")
    else:
        await message.answer("Нажмите /start")
    db.close()