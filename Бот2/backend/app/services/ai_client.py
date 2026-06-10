import openai
from sqlalchemy.orm import Session
from ..config import config
from ..models import Character, Message
from typing import List, Dict, Optional

openai.api_key = config.OPENAI_API_KEY

async def generate_ai_response(
    user_id: int,
    character_id: int,
    scenario_id: Optional[int],
    message_text: str,
    db: Session,
    ooc_mode: bool = False
) -> str:
    # Загружаем персонажа
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        return "Персонаж не найден."

    # Загружаем последние 10 сообщений из этого чата
    from ..models import Chat, Message as DBMessage
    chat = db.query(Chat).filter(Chat.user_id == user_id, Chat.character_id == character_id).first()
    history: List[Dict[str, str]] = []
    if chat:
        recent = db.query(DBMessage).filter(DBMessage.chat_id == chat.id).order_by(DBMessage.created_at.desc()).limit(10).all()
        for msg in reversed(recent):
            history.append({"role": msg.role, "content": msg.content})

    system_prompt = character.system_prompt
    if scenario_id and character.scenarios:
        # Ищем сценарий по id (JSON хранит список)
        scenario = next((s for s in character.scenarios if s.get("id") == scenario_id), None)
        if scenario:
            system_prompt += f"\n\nТекущий сценарий: {scenario.get('intro', '')}"

    if ooc_mode:
        system_prompt = "Ты — полезный ассистент, отвечай кратко и по делу."

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": message_text})

    try:
        response = await openai.ChatCompletion.acreate(
            model=config.OPENAI_MODEL,
            messages=messages,
            temperature=0.85,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка AI: {str(e)}"

async def simple_chat(text: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": text}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except:
        return "Извините, сейчас не могу ответить."