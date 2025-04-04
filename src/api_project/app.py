from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select

from api_project.database import get_session
from api_project.models import User
from api_project.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

api = FastAPI()


@api.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}


@api.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            ((User.email == user.email) | (User.username == user.username))
        )
    )

    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='User with this email already exists',
            )
        elif db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='User with this username already exists',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        name=user.name,
        password=user.password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@api.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(limit: int = 10, session=Depends(get_session)):
    user = session.scalars(select(User).limit(limit))
    return {'users': user}


@api.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    db_user.username = user.username
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@api.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
