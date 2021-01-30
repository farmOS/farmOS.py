from enum import Enum
from typing import Any, Dict, List, Optional, Union
import json

from pydantic import BaseModel, Field, validator

from .session import OAuthSession

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

    @validator("uri", pre=True, always=True)
    def check_uri_or_endpoint(cls, uri, values):
        endpoint = values.get("endpoint", None)
        if uri is None and endpoint is None:
            raise ValueError("Either uri or endpoint is required.")
        return uri

    @validator("body", pre=True)
    def serialize_body(cls, body):
        if not isinstance(body, str):
            return json.dumps(body)
        return body


class SubrequestsBlueprint(BaseModel):
    __root__: List[Subrequest] = Field(
        ...,
        description="Describes the subrequests payload format.",
        title="Subrequests format",
    )


class Format(str, Enum):
    html = "html"
    json = "json"


class SubrequestsBase(object):
    """Class for handling subrequests"""

    subrequest_path = "subrequests"

    def __init__(self, session: OAuthSession):
        self.session = session

    def send(
        self,
        blueprint: Union[SubrequestsBlueprint, List],
        format: Optional[Union[Format, str]] = Format.json,
    ):

        if isinstance(blueprint, List):
            blueprint = SubrequestsBlueprint.parse_obj(blueprint)

        # Modify each sub-request as needed.
        for sub in blueprint.__root__:
            # Build the URI if an endpoint is provided.
            if sub.uri is None and sub.endpoint is not None:
                sub.uri = "{}/{}".format(self.session.hostname, sub.endpoint)

            # Auto populate headers for each sub-request.
            if "Accept" not in sub.headers:
                sub.headers["Accept"] = "application/vnd.api+json"
            if sub.body is not None and "Content-Type" not in sub.headers:
                sub.headers["Content-Type"] = "application/vnd.api+json"

        headers = {"Content-Type": "application/json"}

        params = {}
        if format == Format.json.value:
            params = {"_format": "json"}

        # Generate the json to send. It is important to use the .json() method
        # of the model for correct serialization.
        json = blueprint.json(exclude={"subrequest": {"endpoint"}}, exclude_none=True)
        options = {"data": json}

        response = self.session.http_request(
            method="POST",
            path=self.subrequest_path,
            options=options,
            params=params,
            headers=headers,
        )

        # Return a json response if requested.
        if format == Format.json.value:
            return response.json()

        return response
