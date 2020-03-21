FROM python:3.6-alpine as base

FROM base as build

COPY src/requirements.txt ./requirements.txt
COPY requirements_local.txt ./requirements_local.txt
RUN pip install -r ./requirements.txt -r ./requirements_local.txt

FROM python:3.6-alpine as release

ARG FLASK_ENV
ENV FLASK_ENV=${FLASK_ENV}

WORKDIR /app

RUN addgroup -S app && \
    adduser -S -G app app && \
    chown -R app:app /app && \
    apk --update --no-cache add curl    

COPY . /app/
COPY --from=BUILD /usr/local/ /usr/local

USER app

CMD python src/main.py
