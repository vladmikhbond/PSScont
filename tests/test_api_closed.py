from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Problem

import pytest
from datetime import datetime, timedelta, timezone
import jwt
from app.routers.token_router import SECRET_KEY, ALGORITHM

# Функція для створення тестового токена
def create_test_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {"sub": username, "exp": expire, "role": "student"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def token():
    return create_test_token("py")


client = TestClient(app)

def test_get_problems_lang(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/problems/lang/js", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 280
    
    
def test_get_problems_id(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/problems/4b1aa936-9d3c-40a8-b4c8-154c2d2ccecd", headers=headers)
    assert response.status_code == 200
    assert response.json()['attr'] == "js/01 Числа та вирази"
    
    
def test_post_problems(token):
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
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/problems", json=body, headers=headers)   
    assert response.status_code == 200
    assert len(response.text) == 38         # 38 = length of uuid + 2
    
def test_put_problems(token):
    body = {
        "id": "4b1aa936-9d3c-40a8-b4c8-154c2d2ccecd",
        "title": "TEST TEST TEST TEST TEST TEST TEST TEST Скільки секунд",
        "attr": "js/01 Числа та вирази",
        "lang": "js",
        "cond": "Напишіть програму, яка підрахує, скільки секунд у 2024 році.\r\nРезультат збережіть у змінній sec.\r\n",
        "view": "let sec = ",
        "hint": "//BEGIN\r\nlet sec = \r\n//END",
        "code": "//BEGIN\r\nlet sec = 366 * 24 * 60 * 60\r\n//END\r\nif (sec != 366 * 24 * 60 * 60) \r\n   throw new Error('Wrong');\r\nthrow new Error('OK');",
        "author": "opr"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put("/api/problems", json=body, headers=headers)  
    assert response.status_code == 200
    assert response.text == '"4b1aa936-9d3c-40a8-b4c8-154c2d2ccecd"'

from app.data_alch import add_problem
    
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
