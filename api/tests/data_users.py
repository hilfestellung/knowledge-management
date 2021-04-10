from km.database import get_db


def setup(client):
    response = client.put('/authentication/register',
                          data={'email': 'login@test.org', 'password': 'some', 'firstName': 'Login',
                                'lastName': 'User'})
    assert response.status_code == 201
