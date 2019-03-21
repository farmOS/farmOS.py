from urllib.parse import urlparse, parse_qs

from .session import APISession

class farmOS:

    """Create a new farmOS instance.

    Keyword Arguments:
    hostname - the farmOS hostname (without protocol)
    username - the farmOS username
    password - the farmOS user's password

    Attributes:
    session - an APISession object that handles HTTP requests

    """

    def __init__(self, hostname, username, password):
        self.session = APISession(hostname, username, password)

    def authenticate(self):
        """Authenticates with the farmOS site.

        Returns True or False indicating whether or not
        the authentication was successful
        """
        return self.session.authenticate()

    def get_areas(self, filters={}):
        """Retirieve all farm area get_records"""
        return self.get_terms('farm_areas')

    def get_terms(self, vocabulary, filters={}):
        """Generic method for retrieving terms from a given vocabulary."""
        filters['bundle'] = vocabulary
        return self.get_records('taxonomy_term', filters)

    def get_records(self, entity_type, filters={}):
        """"Generic method for retrieving a list of records from farmOS."""
        data = self._get_record_data(entity_type, filters)

        if ('list' in data):
            return data['list']

        return []

    def page_count(self, entity_type, filters={}):
        """
        Determines how many pages of records are available for
        a given entity type and filter(s).
        """
        pages = 0

        data = self.get_record_data(entity_type, filters)

        # If the 'last' page is not set, return 0
        if ('last' not in data):
            return pages

        # The number of pages is the last page + 1
        parsed_url = urlparse(data['last'])
        pages = parse_qs(parsed_url.query)['page'][0]
        return int(pages) + 1

    def _get_record_data(self, entity_type, filters={}):
        """Retrieve raw record data from the farmOS API."""
        path = entity_type + '.json'

        if filters and 'id' in filters:
            path = entity_type + '/' + filters['id'] + '.json'

        response = self.session.http_request(path=path, params=filters)
        if (response.status_code == 200):
            return response.json()

        return []
