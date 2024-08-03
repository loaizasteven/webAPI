# 
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./localDevAPI /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
