from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from ...services.economy import get_or_create_user, add_gems, add_energy
from ...config import config

router = APIRouter()

@router.get("/packs")
def get_packs():
    return {
        "gems": config.GEMS_PACKS,
        "energy": {"small": 20, "medium": 50, "large": 120},
        "energy_prices": {"small": 10, "medium": 20, "large": 40}  # в Stars
    }

@router.post("/buy_gems")
def buy_gems(tg_id: int, gems_amount: int, stars_paid: int, db: Session = Depends(get_db)):
    # Проверка соответствия цены (в реальности вызывается из successful_payment)
    expected = config.GEMS_PACKS.get(gems_amount)
    if expected != stars_paid:
        raise HTTPException(400, "Price mismatch")
    user = get_or_create_user(db, tg_id)
    add_gems(db, user, gems_amount)
    return {"new_balance": user.gems}