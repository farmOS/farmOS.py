from .session import APISession

class BaseAPI(object):
    def __init__(self, session, entity_type=None):
        self.session = session
        self.entity_type = entity_type
        self.filters = {}

    def _get_record_data(self, filters={}):
        """Retrieve raw record data from the farmOS API."""

        # Determine if filters is an int (id) or dict (filters object)
        if isinstance(filters, int):
            # Set path to return record type by specific ID
            path = self.entity_type + '/' + str(filters) + '.json'

            response = self.session.http_request(path=path)
        elif isinstance(filters, dict):
            # Set path to return record type + filters
            path = self.entity_type + '.json'
            # Combine instance filters and filters from the method call
            filters = {**self.filters, **filters}

            response = self.session.http_request(path=path, params=filters)


        if (response.status_code == 200):
            return response.json()

        return []

    def get(self, filters={}):
        data = self._get_record_data(filters=filters)

        # Check if response contains a list of objects
        if ('list' in data):
            return data['list']
        # Check if response contains an object
        elif len(data) > 0:
            return data
        else:
            return []

class TermAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session=session, entity_type='taxonomy_term')

class LogAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session=session, entity_type='log')

class AssetAPI(BaseAPI):
    def __init__(self, session):
        super().__init__(session=session, entity_type='farm_asset')

class AreaAPI(TermAPI):
    def __init__(self, session):
        super().__init__(session=session)
        self.filters['bundle'] = 'farm_areas'
