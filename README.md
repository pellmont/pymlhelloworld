# pymlhelloworld

[![Build Status](https://travis-ci.org/pellmont/pymlhelloworld.svg?branch=master)](https://travis-ci.org/pellmont/pymlhelloworld)

Sample project for ML pipeline in python

## Setting environment


Clone the template project from GitHub:

```
$ git clone https://github.com/pellmont/pymlhelloworld/
```

This project uses [Docker](https://www.docker.com/) with
[docker-compose](https://docs.docker.com/compose/). These tool enables isolation
and running processes in controlled environment with the needed libraries and
packages.

Two Docker images/containers are used: `nginx` and `web`.
[nginx](https://nginx.org/) is HTTP server used for serving of static content
and doing a reverse proxy for requests handled by Flask application. `web` image
is the image that runs Flask REST API service. 

Configuration of collaboration of these docker containers is defined in the file
`docker-compose.yml`. In `web/Dockerfile` is described the full build of the
`web` docker image.

Building the `web` image consists of:
- installing dependencies
- running all tests
- training model
- producing production Docker image

To run everything locally do:

```
docker-compose up
```

To rebuild and run later after changing the source do:

```
docker-compose up --build
```

If the build was successful the service will be available at http://localhost/


For packaging [pipenv](https://pipenv.readthedocs.io/en/latest/) is used. This
package manager is capable of dependency resolving and locking of environment
using cryptographic hashes of packages.

There are two files maintained by pipenv (in the `web` folder):
- `Pipfile` - contains information about directly required packages and their
  versions.
- `Pipfile.lock` - is the locked environment with installed packages and their
  cryptographic hashes.
  
Keep both files up-to-date in the git repository.

To recreate development environment execute command:

```
pipenv sync --dev
```

To recreate production environment execute command:

```
pipenv sync
```

To install new package:

```
pipenv install mypackage==some_version
```

If version is not provided the latest stable version will be installed, added to
`Pipfile` and locked to `Pipfile.lock`.

To see the dependency graph execute:

```
pipenv graph
```

During docker build `sync` command will be used to recreate environments thus
`Pipfile.lock` must be up-to-date in the git repo to make a proper build.


## REST API


REST API is implemented using [Flask](http://flask.pocoo.org/) with
[Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/) extension.

Endpoints are defined in `web/pymlhelloworld/api` package. There are three
endpoints in this example application. Two are provided by Flask and one is
served directly by nginx.


### `predict` endpoint

See [web/pymlhelloworld/api/predict.py](web/pymlhelloworld/api/predict.py)

The endpoint used for the prediction. It accepts POST request together with the
feature values and the response will be the class together with confidence (in
this case a JSON: `{good_loan:boolean, confidence:float}`). See the generated
Swagger docs for the details.

The params are defined in the file `web/pymlhelloworld/api/predict.py`.


### `healthcheck` endpoint

See [web/pymlhelloworld/api/healthcheck.py](web/pymlhelloworld/api/healthcheck.py)

Used to check the health of the service by calling `predict` endpoint with some
pre-configured data and verifying that the response is both correct and timely.


### `model_info` endpoint

This endpoint is served directly by `nginx` from `web/model_info` folder. In
this folder you provide `model.ipynb` Jupyter Notebook file that will be
transformed to HTML during docker build and served by the `model_info` endpoint
available locally at URL http://localhost/model_info/

### Swagger docs/UI

Flask-RESTplus has a nice capability of generating
[OpenAPI](https://swagger.io/specification/) docs and [Swagger
UI](https://swagger.io/tools/swagger-ui/) directly from the API implementation.
With generated Swagger UI you can use/test the REST API directly from your web
browser.

Generated UI will be available on the root context of the application:
http://localhost/


## Development

### Running the Flask service

To run the service outside of the Docker container (e.g. for debugging purposes)
do:

- this is needed only once inside CLI session

  ```
  pipenv shell
  export FLASK_APP=pymlhelloworld
  ```

- to run Flask do:

  ```
  flask run
  ```

### Model training

If you want to train the model outside of the container (for debugging) from the
`pymlhelloworld/web` folder do:

```
# This is done to fetch the training data only once
wget http://www.ppo2.ch/loan.csv
# Now run the training with
pipenv run python -m pymlhelloworld.train file:loan.csv model.pkl model_info/train.pkl model_info/valid.pkl
```

### Testing

For testing [pytest](https://docs.pytest.org/en/latest/) is used. Tests are
located in the `web/tests` folder. `pytest` is configured in `web/setup.cfg`.

To run the tests do (from `web` folder):

```
pytest
```

Tests will by default run with fake prediction model. To run the tests with
the real model (loaded form pickle file `model.pkl`) do:

```
pytest --real-model
```

See `web/tests/conftest.py` on how to write fixtures and pytest CLI switches.

Code coverage is integrated in the pytest run and set to fail if the coverage is
under 80%.


### Linting

[pylint](https://www.pylint.org/) and [flake8](https://gitlab.com/pycqa/flake8)
are configured for linting. Configuration is in `web/setup.cfg` file. Both tools
are run during docker build and if there are any issue the build is terminated.

To check your code before build do (from `web` folder):

```
pylint --rcfile setup.cfg pymlhelloworld tests
flake8
```
