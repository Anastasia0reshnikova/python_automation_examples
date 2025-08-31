import random
import requests
import time

from pydantic import BaseModel, ValidationError

"""
A) Валидация ответа по контракту
"""
class User(BaseModel):
    id: int
    email: str

def get_user_ok(base: str, uid: int) -> bool:
    r = requests.get(f"{base}/users/{uid}", timeout=10)
    if r.status_code != 200:
        return False
    try:
        User.model_validate(r.json())
        return True
    except ValidationError:
        return False


"""
B) Ретрай с экспонентой и джиттером
"""
def fetch(url, tries=3, base_delay=0.2):
    delay = base_delay
    for i in range(tries):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code >= 500: raise RuntimeError
            return r
        except Exception:
            if i == tries-1: raise
            time.sleep(delay + random.random()*0.2)
            delay *= 2
            return None
    return None


"""
D) Дедуп событий по ключу и времени
"""
def dedup(events):
    # events: list of {"key":..., "ts":..., "value":...}
    best = {}
    for e in events:
        k = (e["key"],)
        if k not in best or e["ts"] > best[k]["ts"]:
            best[k] = e
    return list(best.values())


"""
E) Проверка пагинации
"""
def assert_no_overlap(p1, p2, key="id"):
    s1, s2 = {x[key] for x in p1}, {x[key] for x in p2}
    assert not (s1 & s2)

