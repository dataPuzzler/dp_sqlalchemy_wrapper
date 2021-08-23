import pytest
import sqlalchemy as sa
from dp_sqlalchemy_wrapper.json_fill import JsonFilledDBConfig, JsonFilledDB
from sqlalchemy.orm import clear_mappers
from pathlib import Path


@pytest.fixture(scope="module")
def TestConfig() -> JsonFilledDBConfig:
    
    class TestDBConfig(JsonFilledDBConfig):
        db_url = "sqlite+pysqlite:///:memory:"
        json_fill_dir = Path(__file__).parent.joinpath("testdata").joinpath("json_fill")
            
    return TestDBConfig


@pytest.fixture(scope="function")
def filledTestDB(TestConfig) -> JsonFilledDB:
    from dp_sqlalchemy_wrapper.declarative_util import makeBase

    Base = makeBase()

    class Cat(Base): 
        name = sa.Column(sa.String)
    
    class Dog(Base):
        name = sa.Column(sa.String)
    
    TestConfig.instances_type_mapping = {
        "cats": Cat,
        "dogs": Dog
    }

    testDB = JsonFilledDB(TestConfig, Base)
    yield testDB
    clear_mappers()


def test_json_filled_tables_contains_tables_for_each_of_the_declared_types(filledTestDB):
    filledTestDB.setup_database()
    assert filledTestDB.count_tables_in_db() == 2
