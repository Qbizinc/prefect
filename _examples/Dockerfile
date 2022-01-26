FROM us.gcr.io/ds-cash-production/prefect:3.8

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_CREATE=false

ENV GCP_PROJECT=ds-cash-production

# ENV PYTHONPATH="${PYTHONPATH}:~/Development/prefect/prefect-ds-cash/containers/health_goliath/"

RUN apt-get update && apt-get install -y git
RUN pip install poetry
RUN pip install -U pip

# Install dependencies as a separate step to cache
COPY pyproject.toml poetry.lock /code/

WORKDIR /code
RUN poetry install --no-interaction --no-ansi --no-root

ADD . /code
# RUN poetry install
