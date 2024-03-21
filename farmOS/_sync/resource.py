import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ResourceBase:
    """Base class for JSONAPI resource methods."""

    def __init__(self, client):
        self.client = client
        self.params = {}

    def _get_records(
        self, entity_type, bundle=None, resource_id=None, params=None
    ):
        """Helper function that checks to retrieve one record, one page or multiple pages of farmOS records"""
        if params is None:
            params = {}

        params = {**self.params, **params}

        path = self._get_resource_path(entity_type, bundle, resource_id)

        response = self.client.request(method="GET", url=path, params=params)
        return response.json()

    def get(self, entity_type, bundle=None, params=None):
        return self._get_records(
            entity_type=entity_type, bundle=bundle, params=params
        )

    def get_id(self, entity_type, bundle=None, resource_id=None, params=None):
        return self._get_records(
            entity_type=entity_type,
            bundle=bundle,
            params=params,
            resource_id=resource_id,
        )

    def iterate(self, entity_type, bundle=None, params=None):
        response = self._get_records(
            entity_type=entity_type, bundle=bundle, params=params
        )
        more = True
        while more:
            # TODO: Should we merge in the "includes" info here?
            for resource in response["data"]:
                yield resource
            try:
                next_url = response["links"]["next"]["href"]
                parsed_url = urlparse(next_url)
                next_path = parsed_url._replace(scheme="", netloc="").geturl()
                response = self.client.request(method="GET", url=next_path)
                response = response.json()
            except KeyError:
                more = False

    def send(self, entity_type, bundle=None, payload=None):
        # Default to empty payload dict.
        if payload is None:
            payload = {}

        # Set the resource type.
        payload["type"] = self._get_resource_type(entity_type, bundle)
        json_payload = {
            "data": {**payload},
        }

        # If an ID is included, update the record
        id = payload.pop("id", None)
        if id:
            json_payload["data"]["id"] = id
            logger.debug("Updating record id: of entity type: %s", id, entity_type)
            path = self._get_resource_path(
                entity_type=entity_type, bundle=bundle, record_id=id
            )
            response = self.client.request(
                method="PATCH",
                url=path,
                json=json_payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        # If no ID is included, create a new record
        else:
            logger.debug("Creating record of entity type: %s", entity_type)
            path = self._get_resource_path(entity_type=entity_type, bundle=bundle)
            response = self.client.request(
                method="POST",
                url=path,
                json=json_payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )

        # Handle response from POST requests
        if response.status_code == 201:
            logger.debug("Record created.")

        # Handle response from PUT requests
        if response.status_code == 200:
            logger.debug("Record updated.")

        return response.json()

    def delete(self, entity_type, bundle=None, id=None):
        logger.debug("Deleted record id: %s of entity type: %s", id, entity_type)
        path = self._get_resource_path(
            entity_type=entity_type, bundle=bundle, record_id=id
        )
        return self.client.request(method="DELETE", url=path)

    @staticmethod
    def _get_resource_path(entity_type, bundle=None, record_id=None):
        """Helper function that builds paths to jsonapi resources."""

        if bundle is None:
            bundle = entity_type

        path = "api/" + entity_type + "/" + bundle

        if record_id:
            path += "/" + str(record_id)

        return path

    @staticmethod
    def _get_resource_type(entity_type, bundle=None):
        """Helper function that builds a JSONAPI resource name."""

        if bundle is None:
            bundle = entity_type

        return entity_type + "--" + bundle


class ResourceHelperBase:
    def __init__(self, client, entity_type):
        self.entity_type = entity_type
        self.resource_api = ResourceBase(client=client)

    def get(self, bundle, params=None):
        return self.resource_api.get(
            entity_type=self.entity_type, bundle=bundle, params=params
        )

    def get_id(self, bundle, resource_id, params=None):
        return self.resource_api.get_id(
            entity_type=self.entity_type,
            bundle=bundle,
            resource_id=resource_id,
            params=params,
        )

    def iterate(self, bundle, params=None):
        for item in self.resource_api.iterate(
            entity_type=self.entity_type, bundle=bundle, params=params
        ):
            yield item

    def send(self, bundle, payload=None):
        return self.resource_api.send(
            entity_type=self.entity_type, bundle=bundle, payload=payload
        )

    def delete(self, bundle, id):
        return self.resource_api.delete(
            entity_type=self.entity_type, bundle=bundle, id=id
        )


class AssetAPI(ResourceHelperBase):
    """API for interacting with farm assets"""

    def __init__(self, client):
        # Define 'asset' as the JSONAPI resource type.
        super().__init__(client=client, entity_type="asset")


class LogAPI(ResourceHelperBase):
    """API for interacting with farm logs"""

    def __init__(self, client):
        # Define 'log' as the JSONAPI resource type.
        super().__init__(client=client, entity_type="log")


class TermAPI(ResourceHelperBase):
    """API for interacting with farm Terms"""

    def __init__(self, client):
        # Define 'taxonomy_term' as the farmOS API entity endpoint
        super().__init__(client=client, entity_type="taxonomy_term")


def info(client):
    """Retrieve info about the farmOS server."""

    logger.debug("Retrieving farmOS server info.")
    response = client.request(method="GET", url="api")
    return response.json()
