import pytest
from dp_sqlalchemy_wrapper.base_db import BaseDB
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, registry, clear_mappers
from sqlalchemy.orm.decl_api import DeclarativeMeta

@pytest.fixture(scope="module")
def TestConfig():
    from dp_sqlalchemy_wrapper.base_config import BaseDBConfig
    class TestDBConfig(BaseDBConfig):
        db_url = "sqlite+pysqlite:///:memory:"
    
    return TestDBConfig

@pytest.fixture(scope="function")
def emptyTestDB(TestConfig) -> BaseDB:
    from dp_sqlalchemy_wrapper.declarative_util import makeBase
    Base = makeBase()
    

    class TestDB(BaseDB):
        def _populate_all_tables(self, session):
            return []
    
    testDB = TestDB(TestConfig, Base)
    yield testDB
    clear_mappers()
    

def test_engine_property_return_engine_instance(emptyTestDB: BaseDB):
    assert isinstance(emptyTestDB.engine, Engine)

def test_calling_Session_property_returns_session_instance(emptyTestDB: BaseDB):
    assert isinstance(emptyTestDB.Session(), Session)

def test_calling_registry_property_returns_registry_instance(emptyTestDB: BaseDB):
    assert isinstance(emptyTestDB.registry, registry)

def test_calling_ModelBase_property_return_Base(emptyTestDB: BaseDB):
    assert isinstance(emptyTestDB.Base, DeclarativeMeta)

def test_count_declared_tables(emptyTestDB: BaseDB):
    import sqlalchemy as sa
    assert emptyTestDB.count_declared_tables() == 0
    
    class SampleTable(emptyTestDB.Base):
        sa.Column("key", sa.String, unique=True)
    
    assert emptyTestDB.count_declared_tables() == 1

def test_reset_metadata(emptyTestDB: BaseDB):
    import sqlalchemy as sa

    class SampleTable(emptyTestDB.Base):
        sa.Column("key", sa.String, unique=True)
    
    emptyTestDB.reset_orm_metadata()
    assert emptyTestDB.count_declared_tables() == 0


def test_count_tables_in_db_when_empty(emptyTestDB: BaseDB):
    assert emptyTestDB.count_tables_in_db() == 0


def test_create_tables(emptyTestDB: BaseDB):
    import sqlalchemy as sa
    class SampleTable(emptyTestDB.Base):
        sa.Column("key", sa.String, unique=True)
    emptyTestDB.create_all_tables()
    assert emptyTestDB.count_tables_in_db() == 1


def test_drop_tables(emptyTestDB: BaseDB):
    import sqlalchemy as sa
    class SampleTable(emptyTestDB.Base):
        sa.Column("key", sa.String, unique=True)
    emptyTestDB.create_all_tables()
    emptyTestDB.drop_all_tables()
    assert emptyTestDB.count_tables_in_db() == 0
    assert emptyTestDB.count_declared_tables() == 1