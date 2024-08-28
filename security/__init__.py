import os.path as osp
import os

from fastapi import Depends, HTTPException, status

#Example of accessing the secrets within the container
secret_path = 'run/secrets/oauth_token'

if osp.isfile(secret_path):
    with open('/run/secrets/oauth_token', 'r') as f:
            SECRET_KEY = f.read().strip()
else:
    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1

# Error Class
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