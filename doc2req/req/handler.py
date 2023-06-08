
import typing
from doc2req.model.api import Api
from doc2req.model.point import Point
from doc2req.req.hi import HandlerInterface
from doc2req.req.prep import PrepHelper
from doc2req.req.result import RequestResult

class Handler(HandlerInterface):
    api : Api
    prep_target : type = PrepHelper
    base_url : str

    def overwrite_prep(self, prep : PrepHelper):
        pass

    def __init__(self, url : str, api=None, points:typing.List[Point] = None):
        if api is None:
            self.api = Api(points=points)
        else:
            self.api = api
        self.base_url = url

    def pre_request_callback(self, point : Point, prep : PrepHelper):
        pass

    def post_request_callback(self, point : Point, res : RequestResult):
        pass
        
    def prepReq(
            self, 
            key : typing.Union[tuple, str], 
            *args : typing.List[typing.Any],
            _check : bool=False, 
            **kwargs
        ):
        point = self.api[key]

        if point is None:
            raise ValueError(f"Point {key[0]} not found in api")

        prep : PrepHelper = self.prep_target(point, self)    
        prep.check = _check
        prep.prep(*args,**kwargs)

        return prep

        
        

