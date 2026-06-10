from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import asyncio
import json

from .database import get_db, engine
from .models import Base
from .api.router import api_router
from .bot.dispatcher import bot, dp, set_webhook
from .config import config
from .services.webapp_auth import verify_telegram_auth
from .services.chat_manager import ChatManager

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Veluna API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.WEBAPP_URL, "https://t.me", "https://web.telegram.org"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

# WebSocket менеджер для живого чата
chat_manager = ChatManager()

@app.websocket("/ws/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: int):
    await websocket.accept()
    await chat_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Ожидаем JSON: {"character_id": 1, "text": "hello", "scenario_id": null}
            try:
                msg_data = json.loads(data)
                from .services.ai_client import generate_ai_response
                from .services.economy import deduct_energy
                from .database import SessionLocal
                db = SessionLocal()
                # Проверяем энергию
                user = db.query(User).filter_by(tg_id=user_id).first()
                if user.energy < config.ENERGY_COST_PER_MESSAGE:
                    await websocket.send_text(json.dumps({"error": "Не хватает энергии"}))
                    continue
                deduct_energy(user.tg_id, config.ENERGY_COST_PER_MESSAGE, db)
                # Вызываем AI
                response = await generate_ai_response(
                    user_id=user_id,
                    character_id=msg_data["character_id"],
                    scenario_id=msg_data.get("scenario_id"),
                    message_text=msg_data["text"],
                    db=db
                )
                # Сохраняем сообщения в БД (модели Message, Chat)
                await websocket.send_text(json.dumps({"role": "assistant", "content": response}))
                db.close()
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
    except WebSocketDisconnect:
        chat_manager.disconnect(user_id)

@app.on_event("startup")
async def on_startup():
    await set_webhook()
    # Запускаем фоновые задачи (очистка старых генераций и т.п.)
    asyncio.create_task(background_tasks())

async def background_tasks():
    while True:
        await asyncio.sleep(3600)
        # Логика очистки неактивных задач

@app.get("/health")
async def health():
    return {"status": "ok"}