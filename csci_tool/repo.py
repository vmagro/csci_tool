from jinja2 import Template
import logging
from os import path

logger = logging.getLogger(__name__)


class Repo(object):
    """Repo is a helper for a CSCI project repo
    It has the ability to keep a student's repo up-to-date with a code template
    repo by applying git patches since the last downloaded version.

    Attributes:
        path (PathLike): path to student git repo
    """

    def __init__(self, path, config):
        self.path = path
        self.template_remote = config.template_url

    @staticmethod
    def get_template_repo(course_name):
        """Get template repo for course name.
        Returns:
            (str) URL to the GitHub repo with the course template
        """
        # TODO(vmagro) make this generic for different classes
        return 'https://github.com/vmagrotest/csci_356_template/'

    def init_student_repo(self, template_url, config):
        """Initializes this as a student repo with some basic information such
        as a .gitignore and README.md based on files from the template repo."""
        # clone the template repo into a temporary directory
        # TODO(vmagro) actually clone
        template_repo_path = '/Users/vmagro/tmp/csci_356_template'
        # the template repo has a document initialize_files which contains a
        # list of template paths that need to be filled in with student data as
        # part of the repo initialization
        with open(path.join(template_repo_path, 'initialize_files'), 'r') as f:
            init_files = [l.strip() for l in f.readlines()]
            logger.debug('init template files: %s', init_files)
        # init_files is a list of template file paths that we need to render
        for template_path in init_files:
            # TODO(vmagro) handle files in subdirectory
            suffix_len = len('.template') + 1
            dest_path = path.join(self.path, template_path[:-suffix_len])
            template_path = path.join(template_repo_path, template_path)
            logger.info('Rendering template %s -> %s', template_path, dest_path)
            with open(template_path, 'r') as template:
                template = Template(template.read())
                rendered = template.render(config=config)
                with open(dest_path, 'w') as dest:
                    dest.write(rendered)

    def update_from_branch(self, branch, from_commit):
        """Updates the current branch with commits from branch since from_commit

        Arguments:
            branch (str): template branch to update from
            from_commit (str): git commit hash of latest commit we have
        """
        pass
