from http import HTTPStatus

from fastapi.testclient import TestClient

from api_project.app import api


def test_read_rood_deve_retornar_ok_e_mensagem_hello_world():
    client = TestClient(api)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}
