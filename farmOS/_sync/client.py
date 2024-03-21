from functools import partial

from httpx import Client

from farmOS._sync import resource, subrequests
from farmOS.filter import filter


class FarmClient(Client):
    def __init__(self, hostname, **kwargs):
        super().__init__(base_url=hostname, **kwargs)
        self.info = partial(resource.info, self)
        self.filter = filter
        self.subrequests = subrequests.SubrequestsBase(self)
        self.resource = resource.ResourceBase(self)
        self.log = resource.LogAPI(self)
        self.asset = resource.AssetAPI(self)
        self.term = resource.TermAPI(self)