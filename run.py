# app/cli.py

import click
from flask.cli import with_appcontext
from app import db

@click.command('initdb', help='Initialize the database.')
@with_appcontext
def initdb_command():
    # Import your models here to ensure they are registered with SQLAlchemy
    from app.models import User, Account, Transaction

    # Create all tables
    db.create_all()

    click.echo('Initialized the database.')

# Register the command with Flask CLI
def init_app(app):
    app.cli.add_command(initdb_command)
