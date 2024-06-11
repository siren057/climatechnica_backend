FROM python:3.12-slim-bookworm

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt 

COPY ./src /code/src


CMD ["fastapi", "run", "src/main.py"]