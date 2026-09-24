import hmac
import hashlib
import random
import time
from typing import Tuple

from .config import settings


def _sign(payload: str) -> str:
    return hmac.new(settings.secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()


def new_captcha() -> Tuple[str, str]:
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    answer = a + b
    ts = int(time.time())
    payload = f"{answer}:{ts}"
    token = f"{payload}:{_sign(payload)}"
    return token, f"{a} + {b}"


def verify_captcha(token: str, answer: str, max_age: int = 300) -> bool:
    try:
        parts = token.split(":")
        if len(parts) != 3:
            return False
        expected, ts_s, sig = parts
        if _sign(f"{expected}:{ts_s}") != sig:
            return False
        if int(time.time()) - int(ts_s) > max_age:
            return False
        return str(answer).strip() == expected
    except Exception:
        return False
