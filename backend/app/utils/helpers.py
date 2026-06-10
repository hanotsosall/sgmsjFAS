import random
import string

def generate_promo_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def async_run(coro):
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)