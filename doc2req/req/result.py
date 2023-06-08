
from dataclasses import dataclass
import requests
from doc2req.model.point import Point
from doc2req.req.hi import HandlerInterface
@dataclass
class RequestResult:
    res : requests.Response
    handler : HandlerInterface
    point : Point

    def __post_init__(self):
        self.handler.post_request_callback(self.point, self)
    