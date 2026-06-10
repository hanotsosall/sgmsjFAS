from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from ...database import get_db
from ... import models, schemas
from ...services.ai_client import chat_completion, get_character_system_prompt
from ...services.economy import consume_energy, get_or_create_user
import json

router = APIRouter()

@router.post("/send", response_model=dict)
async def send_message(req: schemas.SendMessageRequest, tg_id: int, db: Session = Depends(get_db)):
    user = get_or_create_user(db, tg_id)
    
    # Проверка энергии
    if not consume_energy(db, user, cost=1):
        raise HTTPException(402, "Not enough energy")
    
    # Получаем персонажа
    character = db.query(models.Character).filter(models.Character.id == req.character_id).first()
    if not character:
        raise HTTPException(404, "Character not found")
    
    # Находим или создаём чат
    chat = db.query(models.Chat).filter(
        models.Chat.user_id == user.id,
        models.Chat.character_id == req.character_id
    ).first()
    if not chat:
        chat = models.Chat(user_id=user.id, character_id=req.character_id, scenario_id=req.scenario_id)
        db.add(chat)
        db.commit()
        db.refresh(chat)
    
    # Сохраняем сообщение пользователя
    user_msg = models.Message(chat_id=chat.id, role="user", content=req.text)
    db.add(user_msg)
    db.commit()
    
    # Получаем историю (последние 10 сообщений)
    history = db.query(models.Message).filter(models.Message.chat_id == chat.id).order_by(models.Message.created_at).limit(10).all()
    
    # Вызов AI
    system_prompt = get_character_system_prompt(character, req.scenario_id)
    ai_response = await chat_completion(system_prompt, history, user.language, req.text)
    
    # Сохраняем ответ
    assistant_msg = models.Message(chat_id=chat.id, role="assistant", content=ai_response)
    db.add(assistant_msg)
    db.commit()
    
    return {"reply": ai_response}

@router.websocket("/ws/{tg_id}")
async def websocket_chat(websocket: WebSocket, tg_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    user = get_or_create_user(db, tg_id)
    active_chat_id = None
    
    try:
        while True:
            data = await websocket.receive_text()
            js = json.loads(data)
            cmd = js.get("cmd")
            
            if cmd == "set_chat":
                active_chat_id = js["chat_id"]
                await websocket.send_json({"type": "system", "content": "Chat activated"})
            
            elif cmd == "message":
                if not active_chat_id:
                    await websocket.send_json({"type": "error", "content": "No active chat"})
                    continue
                
                # Аналогично POST /send, но отправляем через websocket
                # (упрощённо, для полноты можно реализовать)
                # Здесь я покажу принцип, для продакшена лучше использовать единый сервис
                await websocket.send_json({"type": "assistant", "content": "Echo: " + js["text"]})
            
            elif cmd == "generate_image":
                # Запуск генерации через задачу
                from ...services.task_queue import start_generation
                task = start_generation(db, user.id, js["prompt"])
                await websocket.send_json({"type": "task_started", "task_id": task.id})
    
    except WebSocketDisconnect:
        pass