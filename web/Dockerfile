FROM python:3.7-slim as pipenv
LABEL image=pipenv
RUN pip install --no-cache-dir pipenv==2018.11.26

FROM pipenv as pipenv-deps
ENV PIPENV_VENV_IN_PROJECT=True
COPY Pipfile* /app/
WORKDIR /app
RUN pipenv sync

FROM pipenv-deps as builder
LABEL image=base
COPY setup.* /app/
COPY pymlhelloworld /app/pymlhelloworld/
COPY model_info /app/model_info
COPY .coveragerc /app/
WORKDIR /app
RUN pipenv install -e . --skip-lock

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
RUN pipenv run python -m pymlhelloworld.train http://www.ppo2.ch/loan.csv /app/model.pkl model_info/train.pkl model_info/valid.pkl
# --real-model will run the tests using the real prediction model
RUN pipenv run pytest --real-model
RUN pipenv run jupyter nbconvert --to html --stdout --execute model_info/model.ipynb --TagRemovePreprocessor.remove_input_tags={\"invisible\"} --TagRemovePreprocessor.remove_all_outputs_tags={\"invisible\"} --TagRemovePreprocessor.remove_input_tags={\"output\"} > model_info/index.html


FROM builder
MAINTAINER Pascal Pellmont <github@ppo2.ch>

WORKDIR /app
COPY --from=train /app/model_info/index.html /app/model_info/
COPY --from=train /app/model.pkl /app/
RUN adduser --system unicorn
USER unicorn
CMD pipenv run gunicorn --workers=5 --bind=0.0.0.0:5000 pymlhelloworld:app



