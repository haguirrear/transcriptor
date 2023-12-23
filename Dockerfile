FROM python:3.11 as base

ENV LANG=C.UTF-8 \
  LC_ALL=C.UTF-8 \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1

ARG POETRY_VERSION=1.6.1

RUN pip install --upgrade pip && curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app

COPY poetry.lock pyproject.toml ./

FROM base as build-tailwind
RUN poetry install --only dev --no-root
COPY ./tailwind.config.js .
COPY ./styles  ./styles
COPY ./templates/ ./templates/
COPY ./makefile .
RUN make poetry-build-css

FROM base as build-python
RUN poetry install --only main --no-root

FROM node:20-slim as build-node
WORKDIR /app

COPY ./yarn.lock .
COPY ./package.json .
COPY ./tsconfig.json .
COPY ./build.mjs .
COPY ./frontend/ ./frontend/

RUN yarn install
RUN yarn build



FROM python:3.11-slim as prod
WORKDIR /app
ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"
# copy poetry install
COPY --from=build-python /app/.venv /app/.venv
COPY . ./
COPY --from=build-tailwind /app/static/css/  ./static/css/
COPY --from=build-node /app/static/js/base.js ./static/js/base.js
EXPOSE 8000
CMD ["./run.sh"]
