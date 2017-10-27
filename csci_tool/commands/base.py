"""Useful snippets for all commands."""
import click

from ..orm import Database

pass_db = click.make_pass_decorator(Database)
