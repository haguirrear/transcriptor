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

COPY ./poetry.lock ./pyproject.toml ./

FROM node:20-slim as build-css-js
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app

RUN apt-get update && apt-get install make

COPY pnpm-lock.yaml .
COPY package.json .
COPY tsconfig.json .
COPY tailwind.config.js .
COPY backend/components/ ./backend/components/
COPY backend/templates/ ./backend/templates/
COPY ./frontend/ ./frontend/
COPY Makefile .

RUN pnpm install --frozen-lockfile
RUN make css
RUN pnpm run build

FROM base as build-python
RUN poetry install --only main --no-root


FROM python:3.11-slim as prod
WORKDIR /app
ENV PATH="/root/.local/bin:/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install make ffmpeg -y
# copy poetry install
COPY --from=build-python /app/.venv /app/.venv
COPY . ./
COPY --from=build-css-js /app/static/styles/main.css  ./static/styles/main.css
COPY --from=build-css-js /app/static/dist/ ./static/dist/
EXPOSE 8000
CMD ["make", "run"]
