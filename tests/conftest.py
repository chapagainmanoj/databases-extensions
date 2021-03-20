import pytest
import sqlalchemy as sa
from databases import Database
from sqlalchemy.sql.functions import func


@pytest.fixture(scope="function")
def database():
    database = Database("sqlite:///test.db")
    assert database
    yield database


@pytest.fixture(scope="function")
def notes():
    metadata = sa.MetaData()

    notes = sa.Table(
        "notes",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("created_on", sa.DateTime, default=func.now()),
        sa.Column("text", sa.String(length=100)),
        sa.Column("completed", sa.Boolean),
        sa.Column("modified_on", sa.DateTime, onupdate=func.utc_timestamp()),
    )
    yield notes


@pytest.fixture(scope="function")
def notes_data():
    notes = [
        {"text": "Todo 1", "completed": True},
        {"text": "Todo 2", "completed": False},
        {"text": "Todo 3", "completed": True},
        {"text": "Todo 4", "completed": False},
        {"text": "Todo 5", "completed": True},
        {"text": "Todo 6", "completed": True},
    ]
    yield notes
