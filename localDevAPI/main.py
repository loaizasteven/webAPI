from typing import Union, Annotated

import os
import sys
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

file_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(file_dir)
sys.path.insert(0, root_dir)

from security.classstructures import Token, Item, User
from security.authentication import (
    get_current_active_user, 
    authenticate_user, 
    create_access_token, 
    fake_users_db
)
from security import ACCESS_TOKEN_EXPIRE_MINUTES


app = FastAPI(
    title="Web Application with Authentication",
    description='This is a sample web app using fastAPI',
    summary="Add Summary Here",
    version="0.0.2",
    contact={
        "name": "Steven Loaiza",
        "url": "http://github.com/loaizasteven",
    },
)

@app.get("/")
def read_roots():
    return {"message": "This app is serving locally @ localhost/docs"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
