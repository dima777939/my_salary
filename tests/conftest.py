import os
import pytest
from starlette.testclient import TestClient
from sqlalchemy_utils import create_database, drop_database
from alembic import command
from alembic.config import Config

from api.db import DATABASE_URL
from api.main import app


@pytest.fixture(scope="module")
def setup_db():
    try:
        create_database(DATABASE_URL)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        alembic_cfg = Config(os.path.join(base_dir, "alembic.ini"))
        command.upgrade(alembic_cfg, "head")
        yield DATABASE_URL
    finally:
        drop_database(DATABASE_URL)


@pytest.fixture()
def client(setup_db):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def data_user_su():
    return {
        "username": "dima",
        "first_name": "string",
        "last_name": "string",
        "email": "user@example.com",
        "is_active": True,
        "is_staff": True,
        "is_superuser": True,
        "password": "password",
        "rate_an_hour": 500,
        "date_increased": "2023-06-11",
    }


@pytest.fixture()
def request_data_auth_su():
    return {"username": "dima", "password": "password"}


@pytest.fixture()
def request_data_auth_user():
    return {"username": "ivan1", "password": "ipassword1"}


@pytest.fixture()
def data_new_user():
    return {
        "username": "ivan",
        "first_name": "istring",
        "last_name": "istring",
        "email": "ivan@example.com",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False,
        "password": "ipassword",
        "rate_an_hour": 500,
        "date_increased": "2023-10-11",
    }


@pytest.fixture()
def data_new_user1():
    return {
        "username": "ivan1",
        "first_name": "istring1",
        "last_name": "istring1",
        "email": "ivan1@example.com",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False,
        "password": "ipassword1",
        "rate_an_hour": 500,
        "date_increased": "2023-10-11",
    }


@pytest.fixture()
def data_update_new_user():
    return {
        "username": "ivan",
        "first_name": "istring",
        "last_name": "istring",
        "email": "ivan@example.com",
        "is_active": True,
        "is_staff": True,
        "is_superuser": False,
        "password": "ipassword",
        "rate_an_hour": 1000,
        "date_increased": "2024-10-11",
    }


@pytest.fixture()
def data_downgrade_new_user():
    return {
        "username": "ivan",
        "first_name": "istring",
        "last_name": "istring",
        "email": "ivan@example.com",
        "is_active": False,
        "is_staff": False,
        "is_superuser": False,
        "password": "ipassword",
        "rate_an_hour": 1000,
        "date_increased": "2024-10-11",
    }
