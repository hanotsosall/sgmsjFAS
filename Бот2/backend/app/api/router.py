from fastapi import APIRouter
from .endpoints import characters, chat, user, shop, tasks

api_router = APIRouter()
api_router.include_router(characters.router, prefix="/characters", tags=["characters"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(shop.router, prefix="/shop", tags=["shop"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])