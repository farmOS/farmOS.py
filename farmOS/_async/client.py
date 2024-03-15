from functools import partial

from httpx import AsyncClient

from farmOS._async import resource, subrequests
from farmOS.filter import filter


class AsyncFarmClient(AsyncClient):
    def __init__(self, hostname, **kwargs):
        super().__init__(base_url=hostname, **kwargs)
        self.info = partial(resource.info, self)
        self.filter = filter
        self.subrequests = subrequests.SubrequestsBase(self)
        self.resource = resource.ResourceBase(self)
        self.log = resource.LogAPI(self)
        self.asset = resource.AssetAPI(self)
        self.term = resource.TermAPI(self)
