from typing import Union, Annotated
import os.path as osp

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

#Example of accessing the secrets within the container
secret_path = 'run/secrets/oauth_token'

if osp.isfile(secret_path):
    with open('/run/secrets/oauth_token', 'r') as f:
            oauth_token = f.read().strip()

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

def get_user(db, username:str):
    if username in db:
        user_dict = db.get(username)
        return UserInDB(**user_dict)

# Oauth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI(
    title="Web Application with Authentication",
    description='This is a sample web app using fastAPI',
    summary="Add Summary Here",
    version="0.0.1",
    contact={
        "name": "Steven Loaiza",
        "url": "http://github.com/loaizasteven",
    },
)

@app.get("/")
def read_roots():
    return {"message": "This app is serving locally @ localhost/docs"}

@app.get("/getToken/")
async def get_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

def fake_decode_token(token):
    """This does not provide any security yet"""
    return get_user(fake_users_db, token)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        # Any HTTP 401 Unauthorized needs to return this header as per specs.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
