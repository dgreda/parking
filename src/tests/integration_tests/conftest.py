import pytest

from parking_api.app import create_app
from parking_api.database import db


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def database():
    db.drop_all()
    db.create_all()
    db.session.commit()
