from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models import Character
from ...schemas import CharacterOut

router = APIRouter()

@router.get("/", response_model=List[CharacterOut])
def get_characters(db: Session = Depends(get_db)):
    chars = db.query(Character).all()
    return chars

@router.get("/{character_id}")
def get_character(character_id: int, db: Session = Depends(get_db)):
    char = db.query(Character).filter(Character.id == character_id).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return {
        "id": char.id,
        "name": char.name,
        "avatar_url": char.avatar_url,
        "large_art_url": char.large_art_url,
        "short_desc": char.short_desc,
        "lore": char.lore,
        "scenarios": char.scenarios,
        "system_prompt": char.system_prompt
    }