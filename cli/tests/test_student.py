import pytest

from csci_tool.student import Student


def test_email_validation():
    """Only USC emails are accepted"""
    with pytest.raises(AssertionError):
        Student(email='v@vinnie.io', github='vmagro')
    Student(email='smagro@usc.edu', github='vmagro')


def test_unix_name():
    """Unix name is extracted from email"""
    s = Student(email='smagro@usc.edu', github='vmagro')
    assert s.unix_name == 'smagro'
