"""
Hello World REST Application.

Assembles all the REST endpoints.
"""

from flask import Flask

from .api import api


app = Flask(__name__,
            static_url_path='/model_info/',
            static_folder='model_info')
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
