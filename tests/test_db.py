import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from api_project.models import User, table_registry


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


def test_create_user(session):
    user = User(
        username='gika',
        name='Giovanni',
        email='giovanni@ze.com',
        password='1234',
    )

    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.username == 'gika'))

    assert result.username == 'gika'
