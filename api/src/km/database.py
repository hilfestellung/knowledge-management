import click
from flask import g, current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

Model = None
Column = None
String = None


def get_db(app=None):
    if not app:
        app = current_app
    if "db" not in g:
        g.db = SQLAlchemy(app)
    return g.db


def init_db():
    global Model, Column, String
    db = get_db()

    Model = db.Model
    Column = db.Column
    String = db.String

    # Import models here
    from km.model import User

    db.create_all()
    db.session.commit()


def close_db(e=None):
    db = g.pop("db", None)


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
