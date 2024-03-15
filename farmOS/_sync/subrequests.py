from typing import List, Optional, Union

from farmOS.subrequests_model import Format, SubrequestsBlueprint


class SubrequestsBase:
    """Class for handling subrequests"""

    subrequest_path = "subrequests"

    def __init__(self, client):
        self.client = client

    def send(
        self,
        blueprint: Union[SubrequestsBlueprint, List],
        format: Optional[Union[Format, str]] = Format.json,
    ):
        if isinstance(blueprint, List):
            blueprint = SubrequestsBlueprint(blueprint)

        # Modify each sub-request as needed.
        for sub in blueprint:
            # Build the URI if an endpoint is provided.
            if sub.uri is None and sub.endpoint is not None:
                sub.uri = sub.endpoint

            # Set the endpoint to None so it is not included in the serialized subrequest.
            sub.endpoint = None

            # Auto populate headers for each sub-request.
            if "Accept" not in sub.headers:
                sub.headers["Accept"] = "application/vnd.api+json"
            if sub.body is not None and "Content-Type" not in sub.headers:
                sub.headers["Content-Type"] = "application/vnd.api+json"

        params = {}
        if format == Format.json.value:
            params = {"_format": "json"}

        # Generate the json to send. It is important to use the .model_dump_json() method
        # of the model for correct serialization.
        blueprint_json = blueprint.model_dump_json(exclude_none=True)

        response = self.client.request(
            method="POST",
            url=self.subrequest_path,
            params=params,
            headers={"Content-Type": "application/json"},
            content=blueprint_json,
        )

        # Return a json response if requested.
        if format == Format.json.value:
            return response.json()

        return response
