import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ResourceBase(object):
    """Base class for JSONAPI resource methods."""

    def __init__(self, session):
        self.session = session
        self.params = {}

    def _get_records(self, entity_type, bundle=None, resource_id=None, params=None):
        """Helper function that checks to retrieve one record, one page or multiple pages of farmOS records"""
        if params is None:
            params = {}

        params = {**self.params, **params}

        path = self._get_resource_path(entity_type, bundle, resource_id)

        response = self.session.http_request(path=path, params=params)
        return response.json()

    def get(self, entity_type, bundle=None, params=None):
        return self._get_records(entity_type=entity_type, bundle=bundle, params=params)

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
            for record in response["data"]:
                yield record
            try:
                next_url = response["links"]["next"]["href"]
                response = self.session._http_request(url=next_url)
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
        options = {"json": json_payload}

        # If an ID is included, update the record
        id = payload.pop("id", None)
        if id:
            json_payload["data"]["id"] = id
            logger.debug("Updating record id: of entity type: %s", id, entity_type)
            path = self._get_resource_path(
                entity_type=entity_type, bundle=bundle, record_id=id
            )
            response = self.session.http_request(
                method="PATCH", path=path, options=options
            )
        # If no ID is included, create a new record
        else:
            logger.debug("Creating record of entity type: %s", entity_type)
            path = self._get_resource_path(entity_type=entity_type, bundle=bundle)
            response = self.session.http_request(
                method="POST", path=path, options=options
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
        return self.session.http_request(method="DELETE", path=path)

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


class ResourceHelperBase(object):
    def __init__(self, session, entity_type):
        self.entity_type = entity_type
        self.resource_api = ResourceBase(session=session)

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
        return self.resource_api.iterate(
            entity_type=self.entity_type, bundle=bundle, params=params
        )

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

    def __init__(self, session):
        # Define 'asset' as the JSONAPI resource type.
        super().__init__(session=session, entity_type="asset")


class LogAPI(ResourceHelperBase):
    """API for interacting with farm logs"""

    def __init__(self, session):
        # Define 'log' as the JSONAPI resource type.
        super().__init__(session=session, entity_type="log")


class TermAPI(ResourceHelperBase):
    """API for interacting with farm Terms"""

    def __init__(self, session):
        # Define 'taxonomy_term' as the farmOS API entity endpoint
        super().__init__(session=session, entity_type="taxonomy_term")


def info(session):
    """Retrieve info about the farmOS server."""

    logger.debug("Retrieving farmOS server info.")
    response = session.http_request("api")
    return response.json()


def filter(path, value, operation="="):
    """Helper method to build JSONAPI filter query params."""

    # TODO: Validate path, value, operation?
    # TODO: Support filter groups.
    # TODO: Support revision filters, are these edge cases?
    # TODO: Support "pagination" query params? Separate method?
    # TODO: Support "sort" query params? Separate method?
    # TODO: Support "includes" query params? Separate method?

    filters = {}

    # If the operation is '=', only one query param is required.
    if operation == "=":
        param = f"filter[{path}]"
        filters[param] = value
    # Else we need a query param for the path, operation, and value.
    else:
        # TODO: Use a unique identifier instead of using "condition"
        # otherwise the same path cannot be filtered multiple times.
        base_param = f"filter[{path}_{operation.lower()}][condition]"

        path_param = base_param + "[path]"
        filters[path_param] = path

        op_param = base_param + "[operator]"
        filters[op_param] = operation

        value_param = base_param + "[value]"
        if operation in ["IN", "NOT IN", ">", "<", "<>", "BETWEEN"]:
            value_param += "[]"
        filters[value_param] = value

    return filters
