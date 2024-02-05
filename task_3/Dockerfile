FROM python:3.10.12
LABEL maintainer="Ilgiz Rakhimianov <i@rakhimianov.ru>"

ARG DEPENDENCIES="curl vim locales tzdata postgresql-client"
RUN apt-get update && apt-get install -y $DEPENDENCIES

RUN sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG ru_RU:ru
ENV LANGUAGE ru_Ru:ru
ENV LC_ALL ru_RU.UTF-8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /opt/app
WORKDIR /opt/app

ARG POETRY_VERSION="1.7.1"
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --without test

EXPOSE 80

VOLUME /media/
VOLUME /static/

CMD rm -rf static; ln -s /static static; \
    rm -rf media; ln -s /media media; \
    python3 ./manage.py migrate; \
    python3 ./manage.py collectstatic --noinput
