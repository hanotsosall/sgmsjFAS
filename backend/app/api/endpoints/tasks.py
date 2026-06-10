from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from ...models import User
from ...services.economy import add_energy
import httpx

router = APIRouter()

@router.post("/complete/{task_id}")
async def complete_task(task_id: str, tg_id: int, db: Session = Depends(get_db)):
    # task_id может быть "subscribe_channel", "visit_bot", "daily_login"
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    if task_id == "subscribe_channel":
        # Проверяем через Telegram API, подписан ли пользователь на канал @veluna_channel
        async with httpx.AsyncClient() as client:
            url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/getChatMember"
            params = {"chat_id": "@veluna_channel", "user_id": tg_id}
            resp = await client.get(url, params=params)
            data = resp.json()
            if data.get("ok") and data["result"]["status"] in ["member", "administrator", "creator"]:
                add_energy(tg_id, 10, db)
                return {"reward": "energy", "amount": 10}
            else:
                raise HTTPException(400, "Not subscribed")
    elif task_id == "daily_login":
        # Проверить, не получал ли уже сегодня
        add_energy(tg_id, 15, db)
        return {"reward": "energy", "amount": 15}
    else:
        raise HTTPException(400, "Unknown task")