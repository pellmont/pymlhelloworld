#!/bin/sh
jupyter nbconvert --to script model/model.ipynb --stdout > model/model.py
