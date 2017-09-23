"""Useful snippets for all commands."""
import click

from ..api import Api


pass_api = click.make_pass_decorator(Api)
