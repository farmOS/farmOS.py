from .session import APISession

class BaseAPI(object):
    def __init__(self, session, entity_type=None):
        self.session = session
        self.entity_type = entity_type
        self.filters = {}

    def _get_record_data(self, filters={}):
        """Retrieve raw record data from the farmOS API."""
        # Combine instance filters and filters from the method call
        filters = {**self.filters, **filters}

        path = self.entity_type + '.json'

        response = self.session.http_request(path=path, params=filters)
        if (response.status_code == 200):
            return response.json()

        return []

    def get(self, filters={}):
        data = self._get_record_data(filters=filters)

        if ('list' in data):
            return data['list']

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
