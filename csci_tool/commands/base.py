"""Useful snippets for all commands."""
import click

# from ..config import Config
class Config:
    pass

pass_config = click.make_pass_decorator(Config)
