from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from api_project.app import api


@pytest.fixture
def client():
    return TestClient(api)


def test_read_rood_deve_retornar_ok_e_mensagem_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'johndoe',
            'name': 'John Doe',
            'email': 'John@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'username': 'johndoe',
        'name': 'John Doe',
        'email': 'John@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'johndoe',
                'name': 'John Doe',
                'email': 'John@example.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'johndoe',
            'name': 'John Doe',
            'email': 'John@example.com',
            'password': 'secret',
            'id': 1,
        },
    )

    assert response.json() == {
        'username': 'johndoe',
        'name': 'John Doe',
        'email': 'John@example.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
