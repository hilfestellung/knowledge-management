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
