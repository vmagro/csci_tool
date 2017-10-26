from . import orm
from .orm import Field, Model
import pytest


class Student(Model):
    usc_id = Field()
    usc_email = Field()
    github_username = Field()
    test_default = Field(default='default-value')


def test_model_init_valid():
    """Model sets values to fields declared in class."""
    test_student = Student(usc_id=1234, usc_email='smagro@usc.edu', github_username='vmagro')
    assert test_student.usc_id == 1234
    assert test_student.usc_email == 'smagro@usc.edu'
    assert test_student.github_username == 'vmagro'


def test_model_init_undefined_attr():
    """Model init raises an error if trying to set an undefined attribute."""
    with pytest.raises(AttributeError) as err:
        Student(usc_id=1234, usc_email='smagro@usc.edu', github_username='vmagro', asdf=True)
    assert err.value.__str__() == 'Model Student does not have Field asdf'


def test_model_init_default():
    """Model init should use default values for attributes that aren't passed."""
    test_student = Student(usc_id=1234, usc_email='smagro@usc.edu', github_username='vmagro')
    assert test_student.test_default == 'default-value'


def test_model_save(mock):
    """Model.save calls db.upsert."""
    mock.patch('csci_tool.orm.ModelMeta.db')
    test_student = Student(usc_id=1234, usc_email='smagro@usc.edu', github_username='vmagro')
    test_student.save()
    assert orm.ModelMeta.db.upsert.called_once_with(test_student)


def test_objects_all():
    """Get all objects with no filter."""
    orm.ModelMeta.db = {}

    # create the class after mocking the db instance
    class Student(Model):
        usc_id = Field()

    mock_students = [Student(usc_id=i) for i in range(10)]
    orm.ModelMeta.db['Student'] = mock_students

    students = Student.objects.all()
    assert students == mock_students
    # get with no filter kwargs should be the same as all()
    students = Student.objects.get()
    assert students == mock_students


def test_objects_get():
    """Get objects with a simple equals filter."""
    orm.ModelMeta.db = {}

    # create the class after mocking the db instance
    class Student(Model):
        usc_id = Field()
        test_field = Field()

        def __eq__(self, other):
            return self.usc_id == other.usc_id

    mock_students = [Student(usc_id=i, test_field=int(i/2)) for i in range(10)]
    orm.ModelMeta.db['Student'] = mock_students

    students = Student.objects.get(test_field=2)
    assert students == mock_students[4:5+1]
