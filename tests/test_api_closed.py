# Вплив на БД: додає тестові задачі і впливає на першу задачу

PROBLEM_ID = "509092a0-c6d9-4ef2-93a8-cf503ee8f951"
PROBLEM_ATTR = "py/01 dummy/"
PROBLEM_SOLV = " c = (year-1) // 100 + 1"
#############################################################

from fastapi.testclient import TestClient
from app.main import app
from app.models.pss_models import Problem

import pytest
from datetime import datetime, timedelta, timezone
import jwt
from app.routers.token_router import SECRET_KEY, ALGORITHM



# Функція для створення тестового токена
def create_test_token(username: str, role: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"sub": username, "exp": expire, "role": role}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def token():
    return create_test_token("tutor", "tutor")



client = TestClient(app)

def test_get_problems_lang(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/problems/lang/py", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 150
    
    
def test_get_problems_id(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/api/problems/{PROBLEM_ID}", headers=headers)
    assert response.status_code == 200
    assert response.json()['attr'] == PROBLEM_ATTR
    
ID = ""

def test_post_problems(token):
    """
    Add New Problem
    """
    body = {
        "title": "TEST TEST Скільки секунд",
        "attr": "TEST js/01 Числа та вирази",
        "lang": "js",
        "cond": "Напишіть програму, яка підрахує, скільки секунд у 2024 році.\r\nРезультат збережіть у змінній sec.\r\n",
        "view": "let sec = ",
        "hint": "//BEGIN\r\nlet sec = \r\n//END",
        "code": "//BEGIN\r\nlet sec = 366 * 24 * 60 * 60\r\n//END\r\nif (sec != 366 * 24 * 60 * 60) \r\n   throw new Error('Wrong');\r\nthrow new Error('OK');",
        "author": "opr"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/problems", json=body, headers=headers)   
    assert response.status_code == 200
    assert len(response.text) == 38         # 38 = length of uuid + 2
    global ID
    ID = response.text[1:-1:]

    
def test_put_problems(token):
    """
    Change an existing problem.
    """
    body = {
        "id": PROBLEM_ID,
        "title": "Какой Век - Яке сторіччя",
        "attr": "py/01 dummy/",
        "lang": "py",
        "cond": """Задан год в переменной year. Определить, к какому веку он относится, например, 2014 год относится к 21 веку. 
Век записать в переменную c.
ВАЖНО: все строки программы начинайте с одного пробела!""",
        "view": """ # Заданный год уже записан в переменную year, не изменяйте ее значение
 c =""",
        "hint": """ Сначала разделим year нацело на 100.
 c = year // 100""",
        "code": """def _f_(year):
#BEGIN
 c = (year-1) // 100 + 1
#END
 return c;

try:_f_(0);
except: raise Exception('Wrong')

if _f_(200) != 2: raise Exception('Wrong. If year == 100 then c = 1. ')
if _f_(3001) == 30: raise Exception('Wrong. For year = 2001 c = 21, not 20.')
if _f_(3001) != 31: raise Exception('Wrong')

raise Exception('OK')""",

        "author": "py"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put("/api/problems", json=body, headers=headers)  
    assert response.status_code == 200
    assert response.text == f'"{PROBLEM_ID}"'

from app.dal import add_problem
    
def test_delete_problems_id(token):
    body = {
        "title": "TEST TEST TEST TEST TEST TEST TEST TEST Скільки секунд",
        "attr": "js/01 Числа та вирази",
        "lang": "js",
        "cond": "Напишіть програму, яка підрахує, скільки секунд у 2024 році.\r\nРезультат збережіть у змінній sec.\r\n",
        "view": "let sec = ",
        "hint": "//BEGIN\r\nlet sec = \r\n//END",
        "code": "//BEGIN\r\nlet sec = 366 * 24 * 60 * 60\r\n//END\r\nif (sec != 366 * 24 * 60 * 60) \r\n   throw new Error('Wrong');\r\nthrow new Error('OK');",
        "author": "opr"
    }
    problem = add_problem(Problem(**body))
    if problem is None: 
        return False
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/api/problems/{problem.id}", headers=headers) 
    assert response.status_code == 200
    assert response.json()['attr'] == "js/01 Числа та вирази"
