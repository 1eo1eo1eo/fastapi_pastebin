FROM python:3.12

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY ./ /app/

RUN chmod a+x docker/*.sh
