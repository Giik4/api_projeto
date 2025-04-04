from sqlalchemy import select

from api_project.models import User


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
