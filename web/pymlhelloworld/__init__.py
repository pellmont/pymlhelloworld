"""
Hello World REST Application.

Assembles all the REST endpoints.
"""

import os

from flask import Flask

from .api import api


this_dir = os.path.dirname(__file__)
static_folder = os.path.abspath(os.path.join(this_dir, '..', 'model_info'))

app = Flask(__name__,
            static_url_path='/model_info',
            static_folder=static_folder)
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
