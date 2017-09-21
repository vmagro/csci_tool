"""Repo utils to work with a repo's files locally."""

from typing import Type

import git

from .models import Student, Repo as DBRepo


class LocalRepo(object):
    """A LocalRepo is a copy of a student repo stored on disk."""

    path: str
    student: Type[Student]

    @staticmethod
    def clone_repo(repo_stub: Type[DBRepo]) -> Type[git.Repo]:
        """Clone a repo to local disk given information from the database."""
        instance = LocalRepo()
        instance.path = 'asdf'
        return instance
