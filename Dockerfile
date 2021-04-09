FROM python:3.9-alpine

ENV PATH /usr/local/bin:$PATH

ENV LANG C.UTF-8
ENV PYTHONIOENCODING 'utf-8'
ENV TZ 'Asia/Yekaterinburg'

USER root
COPY requirements.txt .
RUN apk update \
    && apk add --no-cache --virtual .build-deps build-base python3-dev postgresql-dev \
    && python3 -m pip install --upgrade pip && python3 -m pip install --upgrade setuptools \
    && python3 -m pip install -r requirements.txt --no-cache-dir \
    && rm /requirements.txt \
    && apk --purge del .build-deps \
    && apk add libpq

RUN mkdir -p /app
COPY . /app/
WORKDIR /app

RUN addgroup -g 1000 -S app_group && \
    adduser -u 1000 -S app_user -G app_group
USER app_user

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]