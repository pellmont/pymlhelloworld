FROM python:3.7-alpine as pipenv
LABEL image=pipenv
RUN pip install --no-cache-dir pipenv==2018.11.26

FROM pipenv as builder
LABEL image=base
ENV PIPENV_VENV_IN_PROJECT=True
COPY setup.* /app/
COPY pymlhelloworld /app/pymlhelloworld/
COPY LICENSE /app/
COPY Pipfile* /app/
COPY .coveragerc /app/
WORKDIR /app
RUN pipenv sync \
    && pipenv install --skip-lock .

FROM builder as test
LABEL image=test
COPY tests /app/tests
RUN pipenv sync --dev \
    && pipenv run pytest --cov=pymlhelloworld tests \
    && pipenv run pylint pymlhelloworld tests \
    && pipenv run flake8 --teamcity pymlhelloworld tests

FROM builder
MAINTAINER Pascal Pellmont <github@ppo2.ch>

EXPOSE 5000
RUN adduser --system unicorn
USER unicorn
WORKDIR /app
CMD pipenv run gunicorn --workers=5 --bind=0.0.0.0:5000 pymlhelloworld.app:APP


