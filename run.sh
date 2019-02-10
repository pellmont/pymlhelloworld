#!/bin/bash
pipenv run gunicorn --workers=5 --bind=0.0.0.0:5000 pymlhelloworld.app:APP
