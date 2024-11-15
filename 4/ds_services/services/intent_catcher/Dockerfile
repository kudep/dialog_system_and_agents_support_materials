# syntax=docker/dockerfile:1
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

RUN apt-get update && apt-get install -y \
  curl && \
  rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3 \ 
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -


WORKDIR /app
# copy packages dirs 
COPY common_packages /common_packages
# copy files
COPY services/intent_catcher/pyproject.toml services/intent_catcher/poetry.lock ./

RUN poetry install

# # sync with all service data
COPY services/intent_catcher/ .
#  poetry run fastapi dev --host 0.0.0.0
# CMD ["poetry", "run", "fastapi", "dev", "--host", "0.0.0.0"]
CMD ["poetry", "run", "fastapi", "run", "--host", "0.0.0.0"]
