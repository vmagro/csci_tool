"""Commands for managing courses."""

import click

from .base import pass_api


@click.group()
def course():
    """Command group for courses."""
    pass


@course.command()
@click.option('--name', prompt=True)
@click.option('--github-org', prompt=True)
@click.option('--assignments-repo', prompt=True, default='assignments')
@click.option('--grader-team', prompt=True, default='graders')
@click.option('--student-repo-format', prompt=True, default='hw_{unix_name}')
@click.option('--student-description', prompt=True,
              default='Homework for {preferred_name} {last_name} <{usc_email}>')
@click.option('--comment-on-collect/--no-comment-on-collect', prompt=True, default=True)
@click.option('--private-repos/--no-private-repos', prompt=True, default=True)
@click.option('--bot-email', prompt=True)
@click.option('--bot-username', prompt=True)
@click.option('--bot-token', prompt=True)
@pass_api
def setup(api, name, github_org, assignments_repo, grader_team, student_repo_format,
          student_description, comment_on_collect, private_repos,
          bot_email, bot_token, bot_username):
    """Create a new course on the server."""
    response = api.courses.create(
        validate=False,
        name=name,
        github_org=github_org,
        assignments_repo=assignments_repo,
        grader_team=grader_team,
        student_repo_format=student_repo_format,
        student_description=student_description,
        comment_on_collect=comment_on_collect,
        private_repos=private_repos,
        bot_email=bot_email,
        bot_username=bot_username,
        bot_token=bot_token,
    )
    print(response)
