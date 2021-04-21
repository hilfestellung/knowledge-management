import click
from flask import current_app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

_db = None
Model = None
Table = None
Relationship = None
Backref = None
Column = None
String = None
Integer = None
Boolean = None
DateTime = None


def get_db(app=None):
    global _db
    if not app:
        app = current_app
    if not _db:
        _db = SQLAlchemy(app)
    return _db


def init_db():
    global Model, Table, Relationship, Backref, Column, String, Integer, Boolean, DateTime
    db = get_db()

    Model = db.Model
    Table = db.Table
    Relationship = db.relationship
    Backref = db.backref
    Column = db.Column
    String = db.String
    Integer = db.Integer
    Boolean = db.Boolean
    DateTime = db.DateTime

    # Preload models and register tables here
    from km.model.user import setup as user_setup
    db.create_all()

    # Ensure data
    user_setup()

    # Just to be sure
    db.session.commit()


def close_db(e=None):
    pass


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
