FROM python:3.14-alpine

WORKDIR app/

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main

COPY . .

ENTRYPOINT ["poetry", "run"]