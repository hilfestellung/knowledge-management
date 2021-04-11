import datetime
import json

import jwt as jwt

import data_users
from km.utls import datetime_to_unixtimestamp


def test_register(client, app):
    response = client.put('/authentication/register', data={'email': 'user@test.org', 'password': 'test'})
    assert response.status_code == 400

    response = client.put('/authentication/register',
                          data={'email': 'user@test.org', 'password': 'test', "firstName": 'Test', 'lastName': 'User'})
    assert response.status_code == 201

    assert client.get('/authentication/register').status_code == 405
    assert client.post('/authentication/register').status_code == 405
    assert client.patch('/authentication/register').status_code == 405
    assert client.delete('/authentication/register').status_code == 405

    with app.app_context():
        from km.model import User
        user = User.query.filter_by(email='user@test.org').first()
        assert user is not None
        assert user.password == '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user.name == 'Test User'


def test_login(client, app):
    from km import authentication
    authentication._is_testing = True
    authentication._test_now = datetime.datetime.utcnow()
    data_users.setup(client)

    response = client.put('/authentication/login', data={})
    assert response.status_code == 401
    response = client.put('/authentication/login', data={'email': 'login@test.org', 'password': 'some'})
    assert response.status_code == 200

    expires_at = datetime_to_unixtimestamp(authentication.now_() + authentication.expiration_timespan)
    response_data = json.loads(response.data.decode('utf-8'))
    assert response_data.get('access_token') is not None
    assert response_data.get('expires_at') == expires_at

    decoded_token = jwt.decode(response_data.get('access_token'), app.config['PUBLIC_KEY'], verify=True,
                               audience=app.config['JWT_AUDIENCE'], algorithms=['RS256'])
    assert decoded_token.get('sub') == 'login@test.org'
    assert decoded_token.get('exp') == int(expires_at / 1000)
    assert decoded_token.get('aud') == 'test.org'
    assert decoded_token.get('iat') == int(datetime_to_unixtimestamp(authentication.now_()) / 1000)
    assert decoded_token.get('permissions') == ['concept:read']
