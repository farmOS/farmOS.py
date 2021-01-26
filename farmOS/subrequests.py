from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

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
    uri: str = Field(
        ..., description="The URI where to make the subrequest.", title="URI"
    )
    requestId: Optional[str] = Field(
        None,
        description="ID other requests can use to reference this request.",
        title="Request ID",
    )
    body: Optional[str] = Field(
        None,
        description="The JSON encoded body payload for HTTP requests send a body.",
        title="Body",
    )
    headers: Optional[Dict[str, Any]] = Field(
        None, description="HTTP headers to be sent with the request.", title="Headers"
    )
    waitFor: Optional[List[str]] = Field(
        None,
        description="ID of other requests that this request depends on.",
        title="Parent ID",
    )


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

    def __init__(self, session):
        self.session = session

    def send(
        self,
        blueprint: Union[SubrequestsBlueprint, List],
        format: Optional[Union[Format, str]] = Format.json,
    ):

        if isinstance(blueprint, List):
            blueprint = SubrequestsBlueprint.parse_obj(blueprint)

        headers = {
            "Content-Type": "application/json"
        }

        params = {}
        if format == Format.json.value:
            params = {"_format": "json"}

        options = {"data": blueprint.json(exclude_unset=True)}

        response = self.session.http_request(
            method="POST", path=self.subrequest_path, options=options, params=params, headers=headers
        )
        return response
