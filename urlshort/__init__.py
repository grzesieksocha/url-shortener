from flask import Flask
from urlshort.urlshort import bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'dsfjksbdilfbsklbdf'

    app.register_blueprint(bp)

    return app
