import os

from flask import Flask, jsonify


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def root():
        return jsonify({'version': '0.1'})

    from km.database import init_app
    init_app(app)

    from km import authentication
    app.register_blueprint(authentication.bp)

    return app
