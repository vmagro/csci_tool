from .assignment_utils import assignment_status, import_mutate, import_grade

from os import path


def test_assignment_status_no_mutate(tmpdir):
    """assignment_status detects missing mutate.py."""
    assert not path.exists(path.join(tmpdir, 'mutate.py'))
    status = assignment_status(tmpdir)
    assert status == 'Couldn\'t import mutate.py'


def test_assignment_status_no_mutate_func(tmpdir):
    """assignment_status detects missing mutate function."""
    with open(path.join(tmpdir, 'mutate.py'), 'w') as mutate_file:
        mutate_file.write('')

    status = assignment_status(tmpdir)
    assert status == 'No mutate function'


def test_assignment_status_no_grade(tmpdir):
    """assignment_status detects missing grade.py."""
    with open(path.join(tmpdir, 'mutate.py'), 'w') as mutate_file:
        mutate_file.write('def mutate():\n\tpass')

    status = assignment_status(tmpdir)
    assert status == 'Couldn\'t import grade.py'


def test_assignment_status_no_grade_func(tmpdir):
    """assignment_status detects missing grade function."""
    with open(path.join(tmpdir, 'mutate.py'), 'w') as mutate_file:
        mutate_file.write('def mutate():\n\tpass')
    with open(path.join(tmpdir, 'grade.py'), 'w') as mutate_file:
        mutate_file.write('')

    status = assignment_status(tmpdir)
    assert status == 'No grade function'


def test_import_mutate(tmpdir):
    """Able to import mutate function."""
    with open(path.join(tmpdir, 'mutate.py'), 'w') as mutate_file:
        mutate_file.write('def mutate():\n\tpass')

    mutate = import_mutate(tmpdir)
    assert callable(mutate)


def test_import_grade(tmpdir):
    """Able to import grade function."""
    with open(path.join(tmpdir, 'grade.py'), 'w') as mutate_file:
        mutate_file.write('def grade():\n\tpass')

    grade = import_grade(tmpdir)
    assert callable(grade)


def test_status_ok(tmpdir):
    """Get OK status when assignment is OK."""
    with open(path.join(tmpdir, 'mutate.py'), 'w') as mutate_file:
        mutate_file.write('def mutate():\n\tpass')
    with open(path.join(tmpdir, 'grade.py'), 'w') as mutate_file:
        mutate_file.write('def grade():\n\tpass')

    status = assignment_status(tmpdir)
    assert status == 'OK'
