from datetime import datetime, timedelta, timezone

from security import SECRET_KEY, ALGORITHM
from security.classstructures import UserInDB, TokenData, User

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt 
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from fastapi import Depends, HTTPException, status
from typing import Annotated


# Oauth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
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

def get_user(db, username:str):
    if username in db:
        user_dict = db.get(username)
        return UserInDB(**user_dict)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
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


def fake_decode_token(token):
    """This does not provide any security yet"""
    return get_user(fake_users_db, token)


class ErrorRaise:
    USERNAMEMISSING:HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User missing in paylod",
        headers={"WWW-Authenticate": "Bearer"}
    )
    INVALIDTOKEN:HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate crendentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    USERMISSING:HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User does not have access",
        headers={"WWW-Authenticate": "Bearer"}
    )

    EXPIRESIG:HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token Expired, Reauthenticate",
        headers={"WWW-Authenticate": "Bearer"}
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    exceptions_ = ErrorRaise()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise exceptions_.USERNAMEMISSING
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise exceptions_.EXPIRESIG
    except InvalidTokenError:
        raise exceptions_.INVALIDTOKEN
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise exceptions_.USERMISSING
    return user 

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
