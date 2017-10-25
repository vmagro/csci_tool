"""Functions to do useful operations on assingment directories (mutate.py/grade.py)."""

import importlib.util
import os


class AssignmentError(Exception):
    pass


def assignment_status(path: str) -> str:
    """Create a human-readable string for the assingment status."""
    # try to import mutate.py since that's more important
    try:
        import_mutate(path)
    except AssignmentError as e:
        return str(e)
    # now see if there's a script to grade
    try:
        import_grade(path)
    except AssignmentError as e:
        return str(e)
    # if we were able to import mutate and grade and find a due date, the assignment seems fine
    return 'OK'


def import_name(path: str, name: str):
    """Import the module with name 'name' in the assignment directory at path."""
    module_name = os.path.basename(path) + '.' + name
    spec = importlib.util.spec_from_file_location(module_name, os.path.join(path, name))
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except:
        raise AssignmentError(f'Couldn\'t import {name}')


def import_mutate(path: str):
    """Import the mutate function defined in the assignment directory at path."""
    module = import_name(path, 'mutate.py')
    if not hasattr(module, 'mutate'):
        raise AssignmentError('No mutate function')
    return module.mutate


def import_grade(path: str):
    """Import the grade function defined in the assignment directory at path."""
    module = import_name(path, 'grade.py')
    if not hasattr(module, 'grade'):
        raise AssignmentError('No grade function')
    return module.grade
