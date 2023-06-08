
from doc2req.model.api import Api
from doc2req.model.point import Point


class HandlerInterface:
    api : Api
    prep_target: type
    request_mapping : dict
    base_url : str
    
    def pre_request_callback(self, point : Point, prep ):
        pass

    def post_request_callback(self, point : Point, res ):
        pass

    def overwrite_prep(self, prep ):
        pass