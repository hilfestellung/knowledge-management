from km import create_app


def test_config():
    # assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_root_api(client):
    response = client.get('/')
    assert response.headers.get('content-type') == 'application/json'
    assert response.data == b'{"version":"0.1"}\n'
