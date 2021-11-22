###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.5-alpine as builder

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk --no-cache add postgresql-dev gcc python3-dev musl-dev

# install dependencies
COPY ./req.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r req.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.5-alpine as final

# needed to compile locale files
RUN apk --no-cache add gettext

# create directory for the app user
RUN mkdir -p /home/app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME && mkdir $APP_HOME/static && mkdir $APP_HOME/media
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/req.txt .
RUN pip install --upgrade --no-cache pip && pip install --no-cache /wheels/*

# copy entrypoint files
COPY ./entrypoint.sh ./
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh && \
    chmod +x  $APP_HOME/entrypoint.sh && \
    sed -i 's/Киргизский/Кыргызский/g' /usr/local/lib/python3.8/site-packages/django/conf/locale/ru/LC_MESSAGES/django.po && \
    sed -i 's/Киргизский/Кыргызский/g' /usr/local/lib/python3.8/site-packages/django/conf/locale/ru/LC_MESSAGES/django.mo

# copy project
COPY . $APP_HOME

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
