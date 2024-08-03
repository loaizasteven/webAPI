#!/usr/bin/python    

# Repo webAPI
# env
DIRECTORY="webapi_env"
IMAGE="fastapiimage"
CONTAINER="fastapicontainer"

function activate () {
  source $HOME/git/webAPI/$DIRECTORY/bin/activate
}

if [ -d "$DIRECTORY" ]; then
    activate
else
    echo "Creating venv"
    /usr/local/bin/python3 -m venv "$DIRECTORY"
fi

function docker_build () {
  if [ "$(docker ps -a -q -f name=$CONTAINER)" ]; then
      # cleanup
      echo "cleaning up existing container:"
      docker stop $CONTAINER
      docker rm $CONTAINER
  fi
  # Update image build
  docker build -t $IMAGE .
  # run your container
  docker run -d --name $CONTAINER -p 80:80 $IMAGE
}

# Run on mac with source api_script && authenticate_and_get
function authenticate_and_get () {
  # args
  #  : @required string $1=username
  #  : @required string $2=password
  
  if [ -z "$1" ]; then
    echo "Please supply username"
    exit 500
  elif [ -z "$2" ]; then
    echo "Please supply password"
    exit 500
  else
    echo "API Authentication running...."
  fi

  local USERNAME_="$1"
  local PASSWORD_="$2"
  echo ${USERNAME_}
  echo ${PASSWORD_}
  echo "grant_type=password&username=$USERNAME_&password=$PASSWORD_"

  local TOKEN="$(curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "grant_type=password&username=$USERNAME_&password=$PASSWORD_" \
  | jq -r '.access_token')"

  local OAUTH="$(curl -X 'GET' \
  'http://127.0.0.1:8000/users/me' \
  -H 'accept: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  | jq -r '.hashed_password')"

  export OAUTH_AUTENTICATION=$OAUTH
}
