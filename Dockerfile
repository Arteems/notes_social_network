FROM python:3.12.5-slim



WORKDIR /coin_game_service

RUN apt update \
    && apt upgrade -y  \
    && pip install --no-cache-dir --upgrade poetry

COPY poetry.lock pyproject.toml ./

RUN poetry self add poetry-plugin-export

RUN poetry export --without-hashes -f requirements.txt --output requirements.txt

RUN apt update \
    && apt upgrade -y  \
    && pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./ ./

RUN groupadd -r coin_game_service && useradd --no-log-init -r -g coin_game_service coin_game_service

USER coin_game_service

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]


















