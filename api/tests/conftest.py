import os
import tempfile
from shutil import rmtree

import pytest

from km import create_app
from km.database import init_db


with open(os.path.join(os.path.dirname(__file__), 'config', 'private.key')) as f:
    _private_key = f.read()
with open(os.path.join(os.path.dirname(__file__), 'config', 'public.key')) as f:
    _public_key = f.read()


@pytest.fixture(scope='session')
def app():
    # connection_url = "postgresql+psycopg2://postgres:vL1NVXu6T@postgres:5432/km"
    temp_dir = tempfile.mkdtemp(prefix='km_test.')
    db_path = os.path.join(temp_dir, 'test.db')
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f"sqlite:///{db_path}",
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'JWT_AUDIENCE': 'test.org',
        'PUBLIC_KEY': _public_key,
        'PRIVATE_KEY': _private_key
    })

    with app.app_context():
        init_db()

    yield app

    rmtree(temp_dir)


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()
