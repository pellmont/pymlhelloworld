"""
Hello World REST Application.

Assembles all the REST endpoints.
"""

import os

from flask import Flask, send_from_directory

from .api import api


app = Flask(__name__, static_url_path='')
api.init_app(app)


@app.route('/model_info/<path:path>')
def model_info(path):
    """Serve static files for model description."""
    this_dir = os.path.dirname(__file__)
    target_dir = os.path.join(this_dir, '..', 'model_info')
    return send_from_directory(target_dir, path)


if __name__ == '__main__':
    app.run(debug=True)
