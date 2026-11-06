from test.test_main import client
from main import app
from fastapi import status
from router.auth import get_current_user
from database import SessionLocal
from tables import Todos

def override_get_current_user():
    return {
        'id' : 1,
        'username' : 'testuser'
    }

def test_todo():
    db = SessionLocal()
    # remove old test data if its exist
    db.query(Todos).filter(Todos.id == 69).delete()

    todo = Todos(
        id = 69,
        title = 'Testing',
        description = 'Testing',
        priority = 4,
        completed = True,
        owner_id = 1
    )
    db.add(todo)
    db.commit()

app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_todos():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK

def test_read_specific_todos():
    response = client.get('/todo/69')
    assert response.status_code == status.HTTP_200_OK

def test_create_todo():
    db = SessionLocal()
    # remove old test data if its exist
    db.query(Todos).filter(Todos.id == 69).delete()
    db.commit()

    request_data = {
        "id": 69,
        "title": "Testing",
        "description": "Testing",
        "priority": 1,
        "completed": True
    }
    response = client.post('/create/', json = request_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'massage': 'todo created Successfully..'}

def test_update_todo():
    request_data = {
        "title": "Updated"
    }
    response = client.put('/update/69', json = request_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'massage': 'todo updated Successfully..'}

def test_delete_todo():
    response = client.delete('/delete/69')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'massage': 'todo deleted Successfully..'}