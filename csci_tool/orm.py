"""Basic 'ORM' to load/store data in yaml files."""
import os
import yaml


class Database(object):
    """'Database' made up of yaml file(s)."""

    def __init__(self, path):
        """Create a new database loading either from a single file or a directory."""
        self.path = path
        # self.dict maps Model names to a list of Model instances
        self.dict = self.read_all()

    def read_all(self):
        """Load entire 'db' into memory."""
        # if the file doesn't exist, make it now
        if not os.path.exists(self.path):
            open(self.path, 'a').close()
        # if we only have one file, load from it directly
        if os.path.isfile(self.path):
            self.file = open(self.path, 'w+')
            res = yaml.load(self.file)
            # if the file is empty, yaml.load returns nothing
            if res is None:
                res = {}
            return res
        elif os.path.isdir(self.path):
            # each model is separated into yaml files containing a list of all those models
            raise NotImplementedError()
        assert False, 'Should have either opened a file or a directory of files'

    def __contains__(self, key):
        return key in self.dict

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, val):
        self.dict[key] = val

    def get(self, key, default=None):
        return self.dict.get(key, default)

    def upsert(self, model):
        """Save (insert or update) a model in the db."""
        # write to the file
        self[model.model_name]


class Field(object):
    """Information about a field in a Model."""

    def __init__(self, default=None, primary_key=False, auto_increment=False):
        """Create a new Field instance for a Model."""
        self.default = default
        self.primary_key = primary_key
        self.auto_increment = auto_increment


class Objects(object):
    """Query interface - basically simpler version of Django's .objects."""

    def __init__(self, db, model_name):
        self.db = db
        self.model_name = model_name

    def all(self):
        """Get all Models of given type."""
        return self.db[self.model_name]

    def get(self, **kwargs):
        """Get Model instances with basic filtering options based on kwargs."""
        conditions = []
        for key, val in kwargs.items():
            if key.endswith('__neq'):
                conditions.append(lambda x: getattr(x, key[:-len('__neq')]) == val)
            else:
                conditions.append(lambda x: getattr(x, key) == val)

        def passes_all(x):
            for cond in conditions:
                if not cond(x):
                    return False
            return True

        return [x for x in self.all() if passes_all(x)]


class ModelMeta(type):
    """Metaclass for all Model subclasses."""

    db = None

    def __new__(cls, clsname, superclasses, attributes):
        assert 'objects' not in attributes

        # make sure that we were able to find a primary key, if not we should create a default one
        found_pk = False
        for key, val in attributes.items():
            if type(val) == Field:
                if val.primary_key:
                    found_pk = True
                    break
        if not found_pk:
            # make an integer pk field
            attributes['pk'] = Field(primary_key=True, auto_increment=True)

        # make sure that we have a reference to the db
        if cls.db is None:
            cls.db = Database('./data.yml')

        # add the "attribute property"
        attributes['objects'] = Objects(cls.db, clsname)

        # also add a reference to the Database
        attributes['db'] = cls.db

        # add an attribute to refer to the model name
        attributes['model_name'] = clsname

        return type.__new__(cls, clsname, superclasses, attributes)


class Model(object, metaclass=ModelMeta):
    """Base class for a model that can be stored in our db."""

    def __init__(self, **kwargs):
        """Instantiate a Model with the given keys, setting defaults as needed."""
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise AttributeError(
                    'Model {} does not have Field {}'.format(type(self).__name__, key))
            setattr(self, key, val)
        # check all the keys that we're supposed to have that weren't passed in and set the defaults
        not_passed = set(self.fields.keys()).difference(set(kwargs.keys()))
        for key in not_passed:
            setattr(self, key, self.fields[key].default)

    @property
    def fields(self):
        """Get the fields on this Model."""
        cls = type(self)
        field_names = [field for field in dir(cls) if type(getattr(cls, field)) == Field]
        fields = {name: getattr(cls, name) for name in field_names}
        return fields

    def save(self):
        """Save this new or updated model instance."""
        self.db.upsert(self)
