import os.path as osp
import os

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