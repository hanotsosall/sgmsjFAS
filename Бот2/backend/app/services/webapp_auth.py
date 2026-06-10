import hashlib
import hmac
from urllib.parse import unquote
from .config import config

def verify_telegram_auth(init_data: str) -> dict:
    """
    Проверяет подпись данных от Telegram WebApp.
    Возвращает словарь с полями пользователя или None.
    """
    params = dict(pair.split('=') for pair in init_data.split('&'))
    if 'hash' not in params:
        return None
    received_hash = params.pop('hash')
    # Сортировка ключей
    data_check_string = '\n'.join(f"{k}={unquote(v)}" for k, v in sorted(params.items()))
    secret_key = hashlib.sha256(config.BOT_TOKEN.encode()).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if computed_hash == received_hash:
        return params
    return None