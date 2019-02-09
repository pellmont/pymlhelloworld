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
RUN pip install --no-cache-dir pipenv==2018.11.26 \
    && pipenv install --dev \
    && pipenv run pytest --cov=pymlhelloworld pymlhelloworld/tests \
    && pipenv run pylint pymlhelloworld \
    && pipenv run flake8 --teamcity pymlhelloworld

FROM python:3.7-alpine
MAINTAINER Pascal Pellmont <github@ppo2.ch>
COPY --from=builder /app /app

EXPOSE 5000
RUN adduser --system unicorn
USER unicorn
WORKDIR /app
CMD pipenv run gunicorn --workers=5 --bind=0.0.0.0:5000 pymlhelloworld.app:APP



