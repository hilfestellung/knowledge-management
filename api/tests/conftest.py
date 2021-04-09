import os
import tempfile
from shutil import rmtree

import pytest

from km import create_app
from km.database import init_db


@pytest.fixture
def app():
    print('Init app', flush=True)
    # connection_url = "postgresql+psycopg2://postgres:vL1NVXu6T@postgres:5432/km"
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, 'test.db')
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f"sqlite:///{db_path}",
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
        init_db()

    yield app

    rmtree(temp_dir)


@pytest.fixture
def client(app):
    return app.test_client()
