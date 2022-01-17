from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from loguru import logger

app = FastAPI()
user_storage = []


class User(BaseModel):
    id: int
    username: str
    password: str


@app.get('/get-user-list')
def get_user_list():
    return user_storage


@app.delete('/delete-user/{user_id}')
def delete_user(user_id: int):
    for u in user_storage:
        if u.id == user_id:
            user_storage.remove(u)
            logger.info(f'User {user_id} deleted')
            # return HTTPException(status_code=204, detail=f'user {user_id} deleted')
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=({'details': f'user {user_id} deleted'}))
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'details:': f'user with {user_id} not found'})


@app.post('/create-user')
def create_user(user: User):
    for u in user_storage:
        if user.id == u.id:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'details': f'user {user.id} already created'})
    user_storage.append(user)
    logger.info(f'User {user.id} created')
    return user


@app.put('/update-password/{user_id}')
def update_password(user_id: int, password: Optional[str] = None):
    for u in user_storage:
        if user_id == u.id:
            u.password = password
            logger.info(f'User {user_id} password updated')
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={'details': 'passowrd updated'})
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'details': f'user {user_id} not found'})
