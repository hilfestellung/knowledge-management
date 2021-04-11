import os

from flask import Flask, jsonify


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'config.py')
        app.config.from_pyfile(config_path, silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def root():
        return jsonify({'version': '0.1'})

    with app.app_context():
        from km.database import init_app
        init_app(app)

        if 'SQLALCHEMY_DATABASE_URI' in app.config:
            from km.database import init_db
            init_db()

    from km import authentication
    app.register_blueprint(authentication.bp)

    return app
