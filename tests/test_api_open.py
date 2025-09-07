from fastapi.testclient import TestClient
from app.main import app
from app.models.pss_models import Problem
from tests.test_api_closed import PROBLEM_ID, PROBLEM_SOLV 

client = TestClient(app)

def test_post_check():
    body = {
        "id": PROBLEM_ID,      
        "solving": PROBLEM_SOLV
    }
    response = client.post("/api/check", json=body)    
    assert response.status_code == 200
    assert response.json() == "OK"





