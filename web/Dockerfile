FROM python:3.7-alpine as pipenv
LABEL image=pipenv
RUN echo "manylinux1_compatible = True" > /usr/local/lib/python3.7/_manylinux.py
RUN pip install --no-cache-dir pipenv==2018.11.26

FROM pipenv as builder
LABEL image=base
ENV PIPENV_VENV_IN_PROJECT=True
COPY setup.* /app/
COPY pymlhelloworld /app/pymlhelloworld/
COPY model_info /app/model_info
COPY Pipfile* /app/
COPY .coveragerc /app/
WORKDIR /app
RUN pipenv sync

FROM builder as test
LABEL image=test
COPY tests /app/tests
RUN pipenv sync --dev
RUN pipenv run pytest \
    && pipenv run pylint --rcfile setup.cfg pymlhelloworld tests \
    && pipenv run flake8 --teamcity pymlhelloworld tests

FROM test as train
LABEL image=train
COPY tests /app/tests
RUN pipenv run jupyter nbconvert --to html --stdout model_info/model.ipynb > model_info/index.html


# pytest should be called with --real-model parameter
FROM train as train-test
LABEL image=train-test
RUN pipenv run pytest --real-model


FROM builder
MAINTAINER Pascal Pellmont <github@ppo2.ch>

WORKDIR /app
COPY --from=train /app/model_info/index.html /app/model_info/
RUN adduser --system unicorn
USER unicorn
CMD pipenv run gunicorn --workers=5 --bind=0.0.0.0:5000 pymlhelloworld:app



