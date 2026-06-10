import asyncio
import asyncpg
import json
import os

async def seed():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    # Проверяем, есть ли уже персонажи
    count = await conn.fetchval("SELECT COUNT(*) FROM characters")
    if count == 0:
        characters = [
            {
                "name": "Вэйвэй",
                "avatar_url": "https://example.com/avatars/weiwei.jpg",
                "large_art_url": "https://example.com/art/weiwei_large.jpg",
                "short_desc": "Студентка по обмену из Китая",
                "lore": "Вэйвэй приехала учиться в Токио. Она застенчива, но очень добрая. Обожает аниме и кошек.",
                "scenarios": json.dumps([
                    {"id": 1, "title": "Встреча в кафе", "cover": "https://example.com/scenes/cafe.jpg", "intro": "Вы случайно встречаете Вэйвэй в уютном кафе..."},
                    {"id": 2, "title": "Ночь в северном крыле", "cover": "https://example.com/scenes/night.jpg", "intro": "Тихая ночь, вы гуляете по парку..."}
                ]),
                "system_prompt": "Ты — Вэйвэй, 19 лет, студентка. Ты застенчива, но с радостью общаешься. Используй *действия в звёздочках*, отвечай коротко.",
                "model_price_tier": 1
            },
            {
                "name": "Миюки",
                "avatar_url": "https://example.com/avatars/miyuki.jpg",
                "large_art_url": "https://example.com/art/miyuki_large.jpg",
                "short_desc": "Загадочная нэко-девушка",
                "lore": "Миюки — полукошка, получеловек. Живёт в храме и помогает заблудшим душам.",
                "scenarios": json.dumps([
                    {"id": 1, "title": "Таинственный храм", "cover": "https://example.com/scenes/temple.jpg", "intro": "Вы находите старый храм в лесу..."}
                ]),
                "system_prompt": "Ты — Миюки, кошачий дух. Ты игрива, иногда мурлычешь. Всегда используй ~ня~ в конце предложений.",
                "model_price_tier": 2
            }
        ]
        for char in characters:
            await conn.execute("""
                INSERT INTO characters (name, avatar_url, large_art_url, short_desc, lore, scenarios, system_prompt, model_price_tier)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, char["name"], char["avatar_url"], char["large_art_url"], char["short_desc"], char["lore"], char["scenarios"], char["system_prompt"], char["model_price_tier"])
        print("Seeded characters")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(seed())