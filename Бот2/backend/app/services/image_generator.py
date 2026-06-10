import replicate
from ..config import config

async def generate_image_sync(prompt: str, aspect_ratio: str = "1:1") -> str:
    """
    Синхронная генерация (для тестов). Возвращает URL картинки.
    """
    # Маппинг aspect_ratio для flux
    ratio_map = {
        "square": "1:1",
        "portrait": "2:3",
        "landscape": "3:2"
    }
    ratio = ratio_map.get(aspect_ratio, "1:1")
    output = replicate.run(
        config.FLUX_MODEL,
        input={
            "prompt": prompt,
            "go_fast": True,
            "output_format": "webp",
            "aspect_ratio": ratio,
            "num_outputs": 1
        }
    )
    # output — список URL'ов
    return output[0] if output else None

def generate_image_sync_blocking(prompt: str, aspect_ratio: str = "1:1") -> str:
    """Блокирующая версия для Celery"""
    import replicate
    ratio_map = {"square": "1:1", "portrait": "2:3", "landscape": "3:2"}
    ratio = ratio_map.get(aspect_ratio, "1:1")
    output = replicate.run(
        config.FLUX_MODEL,
        input={
            "prompt": prompt,
            "go_fast": True,
            "output_format": "webp",
            "aspect_ratio": ratio,
            "num_outputs": 1
        }
    )
    return output[0] if output else None