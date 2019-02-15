This is a template REST service for ML applications.

# Modules

# `__init__.py`

This is a bootstrap file which initializes and starts Flask service.

# `api`

This package hosts namespace/endpoint definitions. One file per each namespace.
The root of the package hosts `api` object which is flask-restplus `Api` instance.


# Running functional test

```
pytest tests/functional
```

# Running service

```
export FLASK_APP=pymlhelloworld 
flask run
```


