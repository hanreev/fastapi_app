from app.database.core import SessionDep
from app.models.response import ErrorResponseContent, ResponseContent
from app.models.user import User, UserIn, UserInDB, UserUpdate
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlmodel import select

router = APIRouter(tags=['Users'])


@router.get('/users', response_model=ResponseContent[list[User]])
def get_users(session: SessionDep):
    users = session.exec(select(UserInDB)).all()
    users_out = [user.to_model() for user in users]
    return ResponseContent(message='User list', data=users_out)


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=ResponseContent[User])
def create_user(user_in: UserIn, session: SessionDep):
    user = UserInDB(name=user_in.name, email=user_in.email)
    user.set_password(user_in.password.get_secret_value())
    session.add(user)
    session.commit()
    session.refresh(user)

    return ResponseContent(message='User created', data=user.to_model())


@router.get('/users/{user_id}', response_model=ResponseContent[User], responses={404: {'model': ErrorResponseContent}})
def get_user(user_id: int, session: SessionDep):
    user = session.get(UserInDB, user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponseContent(message='User not found').model_dump(),
        )
    return ResponseContent(message='User detail', data=user.to_model())


@router.put('/users/{user_id}', response_model=ResponseContent[User], responses={404: {'model': ErrorResponseContent}})
def update_user(user_id: int, user_in: UserUpdate, session: SessionDep):
    user = session.get(UserInDB, user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponseContent(message='User not found').model_dump(),
        )
    user.name = user_in.name
    user.email = user_in.email
    if user_in.password:
        user.set_password(user_in.password.get_secret_value())
    session.add(user)
    session.commit()
    session.refresh(user)
    return ResponseContent(message='User detail', data=user.to_model())


@router.delete('/users/{user_id}', response_model=ResponseContent[User], responses={404: {'model': ErrorResponseContent}})
def delete_user(user_id: int, session: SessionDep):
    user = session.get(UserInDB, user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponseContent(message='User not found').model_dump(),
        )
    session.delete(user)
    session.commit()
    return ResponseContent(message='User deleted', data=user.to_model())
