FROM python:3.7-alpine as base

FROM base as build

COPY src/requirements.txt ./requirements.txt
COPY requirements_local.txt ./requirements_local.txt
RUN pip install -r ./requirements.txt -r ./requirements_local.txt

FROM base as release

ARG RUN_ENVIRONMENT
ENV FLASK_ENV=${RUN_ENVIRONMENT}
ENV ENV=${RUN_ENVIRONMENT}

WORKDIR /app

RUN addgroup -S app && \
    adduser -S -G app app && \
    chown -R app:app /app && \
    apk --update --no-cache add curl    

COPY . /app/
COPY --from=BUILD /usr/local/ /usr/local


USER app

CMD python app/src/main.py

ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]