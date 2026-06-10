from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean, BigInteger
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True, nullable=False, index=True)
    language = Column(String(5), default="en")
    energy = Column(Integer, default=30)
    gems = Column(Integer, default=0)
    stars_balance = Column(Integer, default=0)
    ooc_mode = Column(Boolean, default=False)
    current_character_id = Column(Integer, nullable=True)
    current_scenario_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), onupdate=func.now())

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    avatar_url = Column(String(500))
    large_art_url = Column(String(500))
    short_desc = Column(String(200))
    lore = Column(Text)
    scenarios = Column(JSON)  # список сценариев: [{"id":1,"title":"...","cover":"...","intro":"..."}]
    system_prompt = Column(Text)  # базовая системная инструкция
    model_price_tier = Column(Integer, default=1)  # 1=Libra, 2=Phoenix, 3=Orion

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    scenario_id = Column(Integer, nullable=True)
    title = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    role = Column(String(20))  # user, assistant, system
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_generated_image = Column(Boolean, default=False)
    image_url = Column(String(500), nullable=True)

class GenerationTask(Base):
    __tablename__ = "generation_tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prompt = Column(Text)
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    result_url = Column(String(500))
    error = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stars_amount = Column(Integer)  # сколько Stars потрачено
    gems_received = Column(Integer)
    energy_received = Column(Integer)
    payload = Column(String(200))
    status = Column(String(20), default="pending")
    telegram_payment_charge_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())