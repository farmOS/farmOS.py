import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ResourceBase:
    """Base class for JSONAPI resource methods."""

    def __init__(self, client):
        self.client = client
        self.params = {}

    async def _get_records(
        self, entity_type, bundle=None, resource_id=None, params=None
    ):
        """Helper function that checks to retrieve one record, one page or multiple pages of farmOS records"""
        if params is None:
            params = {}

        params = {**self.params, **params}

        path = self._get_resource_path(entity_type, bundle, resource_id)

        response = await self.client.request(method="GET", url=path, params=params)
        return response.json()

    async def get(self, entity_type, bundle=None, params=None):
        return await self._get_records(
            entity_type=entity_type, bundle=bundle, params=params
        )

    async def get_id(self, entity_type, bundle=None, resource_id=None, params=None):
        return await self._get_records(
            entity_type=entity_type,
            bundle=bundle,
            params=params,
            resource_id=resource_id,
        )

    async def iterate(self, entity_type, bundle=None, params=None):
        response = await self._get_records(
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
                response = await self.client.request(method="GET", url=next_path)
                response = response.json()
            except KeyError:
                more = False

    async def send(self, entity_type, bundle=None, payload=None):
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
            response = await self.client.request(
                method="PATCH",
                url=path,
                json=json_payload,
                headers={"Content-Type": "application/vnd.api+json"},
            )
        # If no ID is included, create a new record
        else:
            logger.debug("Creating record of entity type: %s", entity_type)
            path = self._get_resource_path(entity_type=entity_type, bundle=bundle)
            response = await self.client.request(
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

    async def delete(self, entity_type, bundle=None, id=None):
        logger.debug("Deleted record id: %s of entity type: %s", id, entity_type)
        path = self._get_resource_path(
            entity_type=entity_type, bundle=bundle, record_id=id
        )
        return await self.client.request(method="DELETE", url=path)

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

    async def get(self, bundle, params=None):
        return await self.resource_api.get(
            entity_type=self.entity_type, bundle=bundle, params=params
        )

    async def get_id(self, bundle, resource_id, params=None):
        return await self.resource_api.get_id(
            entity_type=self.entity_type,
            bundle=bundle,
            resource_id=resource_id,
            params=params,
        )

    async def iterate(self, bundle, params=None):
        async for item in self.resource_api.iterate(
            entity_type=self.entity_type, bundle=bundle, params=params
        ):
            yield item

    async def send(self, bundle, payload=None):
        return await self.resource_api.send(
            entity_type=self.entity_type, bundle=bundle, payload=payload
        )

    async def delete(self, bundle, id):
        return await self.resource_api.delete(
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


async def info(client):
    """Retrieve info about the farmOS server."""

    logger.debug("Retrieving farmOS server info.")
    response = await client.request(method="GET", url="api")
    return response.json()
