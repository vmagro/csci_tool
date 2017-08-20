import logging
import tempfile
from git import Repo as GitRepo


from .config import Config


logger = logging.getLogger(__name__)


class Repo(object):
    """Repo is a helper for CSCI project repos
    It contains functionality to clone student repos, commit changes and push
    them back to GitHub.

    Attributes:
        path (PathLike): path to student git repo
    """

    def __init__(self, path, config):
        self.path = path

    @staticmethod
    def clone_student_repo(student):
        """Clones a student repo into a temporary directory

        Arguments:
            student (Student)

        Returns:
            PathLike: path to temporary directory where repo was cloned
        """
        logger.info('Cloning repo: %s', student.github)
        tempdir = tempfile.mkdtemp()
        repo_url = student.repo_url
        logger.debug('%s -> %s', repo_url, tempdir)
        GitRepo.clone_from(repo_url, tempdir)
        return tempdir

    @staticmethod
    def meta_repo():
        """Get a reference to the meta repo that contains the templates and
        lists of students

        Returns:
            git.Repo: metadata repo
        """
        config = Config.load_config()
        return GitRepo(config.meta_path)
