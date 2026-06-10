from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    tg_id: int
    language: str = "en"
    energy: int = 30
    gems: int = 0

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    created_at: datetime

class CharacterOut(BaseModel):
    id: int
    name: str
    avatar_url: str
    short_desc: str
    scenarios: List[dict]

class ChatOut(BaseModel):
    id: int
    character_id: int
    character_name: str
    avatar_url: str
    last_message: Optional[str]
    updated_at: datetime

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    is_generated_image: bool = False
    image_url: Optional[str] = None

class SendMessageRequest(BaseModel):
    character_id: int
    text: str
    scenario_id: Optional[int] = None

class GenerateImageRequest(BaseModel):
    prompt: str
    aspect_ratio: str = "1:1"  # square, portrait, landscape