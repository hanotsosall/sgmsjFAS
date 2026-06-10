from .celery_app import celery_app
from ..services.image_generator import generate_image_sync_blocking
from ..services.economy import deduct_gems, add_gems  # на случай отката
from ..database import SessionLocal
from ..models import GenerationTask, User
from aiogram import Bot
from ..config import config
import asyncio

bot = Bot(token=config.BOT_TOKEN)

@celery_app.task(bind=True, max_retries=2)
def generate_image_task(self, prompt: str, user_id: int, chat_id: int, message_id: int, aspect_ratio: str = "1:1"):
    db = SessionLocal()
    # Создаём запись задачи
    task_record = GenerationTask(user_id=user_id, prompt=prompt, status="processing")
    db.add(task_record)
    db.commit()
    try:
        image_url = generate_image_sync_blocking(prompt, aspect_ratio)
        if image_url:
            task_record.status = "completed"
            task_record.result_url = image_url
            db.commit()
            # Отправляем фото пользователю через бота (синхронно, но можно через asyncio.run)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(bot.send_photo(chat_id, photo=image_url, caption=f"✨ Ваш арт по промту: {prompt[:100]}"))
            loop.run_until_complete(bot.delete_message(chat_id, message_id))
        else:
            raise Exception("Генерация не вернула URL")
    except Exception as e:
        task_record.status = "failed"
        task_record.error = str(e)
        db.commit()
        # Возвращаем гемы пользователю (откат)
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.gems += config.GEMS_COST_PER_IMAGE
            db.commit()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bot.send_message(chat_id, f"❌ Ошибка генерации: {str(e)}. Гемы возвращены."))
    finally:
        db.close()