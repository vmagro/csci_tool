FROM python:3.6

# this container image is used to run both the django server through uwsgi and the celery worker
# the CMD is changed in docker-compose to enable this re-use

EXPOSE 8000

# it's safer to not run as root
# create the user now but use it later since we need to be root to set things up
RUN useradd -ms /bin/true uwsgi

RUN pip install -Iv pipenv==8.2.6

# just copy the dependencies at first so that docker can cache the installation
WORKDIR /tmp
COPY Pipfile  ./
COPY Pipfile.lock ./

RUN pipenv install --system

COPY . /app

WORKDIR /app

# it's safer to not run as root
USER uwsgi

CMD "uwsgi -c /app/conf/uwsgi.ini"
