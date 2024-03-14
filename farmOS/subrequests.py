import json
from enum import Enum
from typing import Any, Dict, Iterator, List, Optional, Union

from pydantic import BaseModel, Field, RootModel, field_validator, model_validator

# Subrequests model derived from provided JSON Schema
# https://git.drupalcode.org/project/subrequests/-/blob/3.x/schema.json


class Action(Enum):
    view = "view"
    create = "create"
    update = "update"
    replace = "replace"
    delete = "delete"
    exists = "exists"
    discover = "discover"
    noop = "noop"


class Subrequest(BaseModel):
    action: Action = Field(
        ...,
        description="The action intended for the request. Each action can resolve into a different HTTP method.",
        title="Action",
    )
    endpoint: Optional[str] = Field(
        None,
        description="The API endpoint to request. The base URL will be added automatically.",
        title="Endpoint",
    )
    uri: Optional[str] = Field(
        None, description="The URI where to make the subrequest.", title="URI"
    )
    requestId: Optional[str] = Field(
        None,
        description="ID other requests can use to reference this request.",
        title="Request ID",
    )
    body: Optional[Union[str, dict]] = Field(
        None,
        description="The JSON encoded body payload for HTTP requests send a body.",
        title="Body",
    )
    headers: Optional[Dict[str, Any]] = Field(
        {}, description="HTTP headers to be sent with the request.", title="Headers"
    )
    waitFor: Optional[List[str]] = Field(
        None,
        description="ID of other requests that this request depends on.",
        title="Parent ID",
    )

    @model_validator(mode="after")
    def check_uri_or_endpoint(self):
        # endpoint = values.get("endpoint", None)
        if self.uri is None and self.endpoint is None:
            raise ValueError("Either uri or endpoint is required.")
        return self.uri

    @field_validator("body")
    def serialize_body(cls, body):
        if not isinstance(body, str):
            return json.dumps(body)
        return body


class SubrequestsBlueprint(RootModel):
    root: List

    def __iter__(self) -> Iterator[Subrequest]:
        return iter(self.root)

    def __getitem__(self, item) -> Subrequest:
        return self.root[item]


class Format(str, Enum):
    html = "html"
    json = "json"


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
