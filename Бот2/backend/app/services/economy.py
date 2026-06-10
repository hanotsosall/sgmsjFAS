from sqlalchemy.orm import Session
from ..models import User
from ..database import SessionLocal

def get_user_balance(tg_id: int, db: Session) -> tuple:
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if user:
        return user.energy, user.gems
    return 0, 0

def deduct_energy(tg_id: int, amount: int, db: Session) -> bool:
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if user and user.energy >= amount:
        user.energy -= amount
        db.commit()
        return True
    return False

def add_energy(tg_id: int, amount: int, db: Session):
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if user:
        user.energy += amount
        db.commit()

def deduct_gems(tg_id: int, amount: int, db: Session) -> bool:
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if user and user.gems >= amount:
        user.gems -= amount
        db.commit()
        return True
    return False

def add_gems(tg_id: int, amount: int, db: Session):
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if user:
        user.gems += amount
        db.commit()