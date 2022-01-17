from fastapi.testclient import TestClient

from main import app
client = TestClient(app)


def test_get_user_list():
    response = client.get('/get-user-list')

    assert response.status_code == 200
    assert response.json() == []


def test_create_user():
    response = client.post('/create-user', json={'id': 0, 'username': 'test', 'password': 'test'})

    assert response.status_code == 200


def test_delete_user():
    client.post('/create-user', json={'id': 1, 'username': 'test', 'password': 'test'})
    response_id = client.delete('/delete-user/1')
    response_fake_id = client.delete('delete-user/123')

    assert response_id.status_code == 204
    assert response_fake_id.status_code == 400


def test_update_password():
    client.post('/create-user', json={'id': 2, 'username': 'test', 'password': '123'})
    response = client.put('/update-password/2?password=test')
    response_fakeid = client.put('/update-password/3?password=test')

    assert response.status_code == 201
    assert response_fakeid.status_code == 400
