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
