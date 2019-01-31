"""
Hello World REST Application.

Assembles all the REST endpoints.
"""


from flask import Flask

from flask_restful import Api

APP = Flask(__name__)
API = Api(APP)
