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
COPY run.sh /app/
WORKDIR /app
RUN pipenv sync

FROM builder as test
LABEL image=test
COPY tests /app/tests
RUN pipenv sync --dev
RUN pipenv run pytest \
    && pipenv run pylint pymlhelloworld tests \
    && pipenv run flake8 --teamcity pymlhelloworld tests

FROM test as train
LABEL image=train
RUN [ ! -f /app/model/model.py ] && jupyter nbconvert --to script model.ipynb
RUN python model.py
# TODO: The script should create pickled model

# TODO: Should we make another stage to test trained model?

FROM builder
MAINTAINER Pascal Pellmont <github@ppo2.ch>

EXPOSE 5000
RUN adduser --system unicorn
USER unicorn
WORKDIR /app
# TODO: Copy pickled model file to the appropriate location
CMD ["/app/run.sh"]



