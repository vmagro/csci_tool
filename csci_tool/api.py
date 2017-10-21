import coreapi
import json
import logging
from urllib.request import urlopen

logger = logging.getLogger(__name__)


class Api(object):

    def __init__(self, url=None, client=None, schema=None, action=''):
        if url:
            self.client = coreapi.Client()
            self.schema = self.client.get(url)
            self.action = ''
        else:
            self.client = client
            self.schema = schema
            self.action = action

    def __getattr__(self, name):
        """Allow dot notation for the api.

        Ex: api.students.list expands to client.action(document, ['students', 'list'])
        """
        return Api(client=self.client, schema=self.schema, action=self.action+'/'+name)

    def __call__(self, validate=True, *args, **kwargs):
        """Allow calling as a function when action is defined."""
        assert self.action, 'action must be defined before attempting to call'
        actions = self.action.split('/')[1:]
        response = self.client.action(self.schema, actions, validate=validate, params=kwargs)
        # if the results look like they're paginated, return a generator to auto paginate
        if 'next' in response:
            return paginated_generator(response)
        else:
            return response


def paginated_generator(response):
    """Generate a list of dictionaries from paginated API responses."""
    while True:
        for obj in response['results']:
            yield obj
        if response['next']:
            logger.debug('Loading next page')
            # we're done with results from the current response, get the next one now
            logger.debug('No next page, just returning results')
            response = json.loads(urlopen(response['next']).read())
        else:
            logger.debug('No next page, done now')
            return
