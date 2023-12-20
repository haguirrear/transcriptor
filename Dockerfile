FROM python:3.11 as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

ARG POETRY_VERSION=1.6.1

RUN pip install --upgrade pip && curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app

COPY poetry.lock pyproject.toml ./

FROM base as build
RUN poetry install --only dev --no-root
COPY ./tailwind.config.js .
COPY ./styles  ./styles
COPY ./templates/ ./templates/
COPY ./makefile .
RUN make poetry-build-css


FROM python:3.11-slim as prod
WORKDIR /app
ENV PATH="/root/.local/bin:$PATH"
# copy poetry install
COPY --from=build /root/.local/bin /root/.local/bin
COPY --from=build /root/.local/share/pypoetry /root/.local/share/pypoetry
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main --no-root
COPY . ./
COPY --from=build /app/static/css/  ./static/css/
EXPOSE 8000
CMD ["./run.sh"]
