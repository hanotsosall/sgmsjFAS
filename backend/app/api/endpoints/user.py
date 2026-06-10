from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ... import models, schemas
from ...database import get_db
from ...services.economy import get_or_create_user

router = APIRouter()

@router.get("/me", response_model=schemas.UserOut)
def get_me(tg_id: int, db: Session = Depends(get_db)):
    user = get_or_create_user(db, tg_id)
    return user

@router.get("/balance")
def get_balance(tg_id: int, db: Session = Depends(get_db)):
    user = get_or_create_user(db, tg_id)
    return {"energy": user.energy, "gems": user.gems, "stars": user.stars_balance}

@router.post("/language")
def set_language(tg_id: int, lang: str, db: Session = Depends(get_db)):
    user = get_or_create_user(db, tg_id)
    user.language = lang
    db.commit()
    return {"status": "ok"}