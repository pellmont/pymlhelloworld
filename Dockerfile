FROM python:3.7-slim as pipenv
LABEL image=pipenv
RUN pip install --no-cache-dir pipenv==2018.11.26

FROM pipenv as builder
LABEL image=base
ENV PIPENV_VENV_IN_PROJECT=True
COPY setup.* /app/
COPY pymlhelloworld /app/pymlhelloworld/
COPY model_info /app/model_info
COPY LICENSE /app/
COPY Pipfile* /app/
COPY .coveragerc /app/
WORKDIR /app
RUN pipenv install --skip-lock

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
RUN pipenv run python -m pymlhelloworld.train http://www.ppo2.ch/loan.csv /app/model.pkl
RUN pipenv run jupyter nbconvert --to html --stdout --execute model_info/model.ipynb --TagRemovePreprocessor.remove_input_tags={\"invisible\"} --TagRemovePreprocessor.remove_all_outputs_tags={\"invisible\"} --TagRemovePreprocessor.remove_input_tags={\"output\"} > model_info/index.html


# pytest should be called with --real-model parameter
FROM train as train-test
LABEL image=train-test
RUN pipenv run pytest --real-model


FROM builder
MAINTAINER Pascal Pellmont <github@ppo2.ch>

EXPOSE 5000
WORKDIR /app
COPY --from=train /app/model_info/index.html /app/model_info/
RUN adduser --system unicorn
USER unicorn
CMD pipenv run gunicorn --workers=5 --bind=0.0.0.0:5000 pymlhelloworld:app



