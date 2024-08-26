from datetime import datetime, timedelta, timezone

from security import SECRET_KEY, ALGORITHM, ErrorRaise
from security.classstructures import UserInDB, TokenData, User

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt 
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from fastapi import Depends, HTTPException
from typing import Annotated, Dict, Any

import os
import sys
import os.path as osp

sys.path.insert(0, osp.dirname(osp.dirname(__file__)))
from database import USERDATABASE

# Oauth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def fake_hash_password(password: str):
    return "fakehashed" + password

def get_user(db, username:str):
    if username in db:
        user_dict = db.get(username)
        return UserInDB(**user_dict)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(user_db:Dict, username: str, password: str):
    user = get_user(user_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None, default_expiration: int = 1):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=default_expiration)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def fake_decode_token(token:Any, user_db:Dict = USERDATABASE):
    """This does not provide any security yet"""
    return get_user(user_db, token)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user_db = USERDATABASE
    exceptions_ = ErrorRaise()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise exceptions_.USERNAMEMISSING
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise exceptions_.EXPIRESIG
    # Base Class for all Exceptions
    except InvalidTokenError:
        raise exceptions_.INVALIDTOKEN
    user = get_user(user_db, username=token_data.username)
    if user is None:
        raise exceptions_.USERMISSING
    return user 

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
