
from functools import cached_property
from typing import Callable
import typing
from doc2req.etc.unpackableObj import UnpackableObj
from doc2req.model.parameter import Parameter
from doc2req.model.point import Point
from doc2req.req.hi import HandlerInterface
from doc2req.req.result import RequestResult
import requests
from urllib.parse import urljoin

request_mapping : dict = {
    "get" : requests.get,
    "post" : requests.post,
    "put" : requests.put,
    "delete" : requests.delete,
    "patch" : requests.patch,
}

class PrepHelper:
    point : Point
    body : dict
    url : str
    query : dict
    headers : dict
    handler : HandlerInterface
    path : dict
    result_target : typing.Union[RequestResult,type] = RequestResult
    check : bool = False
    request_method : Callable = None

    def __init__(self, point : Point, handler : HandlerInterface):
        self.point = point
        self.body = {}
        self.url = None
        self.query = {}
        self.headers = {}
        self.handler = handler
        self.path = {}
        self.handler.overwrite_prep(self)

    @cached_property
    # ! using cached property to avoid multiple calls to this function
    def mapping(self):
        return {
            "body" : self.body,
            "query" : self.query,
            "header" : self.headers,
            "path" : self.path,
        }

    def prep(self,*args, _raise_on_unknown : bool = False, **kwargs ):
        # unpack all obj
        for arg in args:
            if not isinstance(arg, UnpackableObj):
                raise ValueError("prep() only accepts UnpackableObj")
            kwargs.update(arg.unpack())

        # extract all valid vars
        valid_vars = {}
        for k, v in kwargs.items():
            if k in self.point.all_vars:
                valid_vars[self.point.all_vars[k]] = v
            elif _raise_on_unknown:
                raise ValueError(f"Invalid variable {k} for point {self.point.name}")
        
        # fill all vars
        for k, v in valid_vars.items():
            k : Parameter
            val = k.check_value(v)
            match k.group:
                case "body":
                    self.body[k.field] = val
                case "query":
                    self.query[k.field] = val
                case "header":
                    self.headers[k.field] = val
                case "path":
                    self.path[k.field] = val
                case _:
                    raise ValueError(
                        f"Invalid group {k.group} for point {self.point.name}"
                    )

    def iter_all_fields(self):
        for k, v in self.body.items():
            # get parameter
            param = self.point.get(k)
            yield "body", k, v, param

        for k, v in self.query.items():
            # get parameter
            param = self.point.get(k)
            yield "query", k, v, param

        for k, v in self.headers.items():
            # get parameter
            param = self.point.get(k)
            yield "header", k, v, param

        for k, v in self.path.items():
            # get parameter
            param = self.point.get(k)
            yield "path", k, v, param
        

    def check_and_finalize_value(self):
        """
        checks value validity and finalize them
        """
        def _required_parse(string :str, param : Parameter, target : dict):
            value = target.get(param.field, None)
            value = param.check_value(value)
            target[param.field] = value

        already_parsed_list = []

        for name, param in self.point.iter_param("mandatory"):
            _required_parse(param.group, param, self.mapping[param.group])
            already_parsed_list.append(param.field)
        
        for where, k, v, param in self.iter_all_fields():
            if param.field in already_parsed_list:
                continue
            self.mapping[where][k] = param.check_value(v)

    
    def prep_request_method(self):
        """
        sets the request method

        can be overwritten
        """
        request : Callable = request_mapping[self.point.type]
        self.request_method = request

    def prep_url(self):
        """
        sets the url

        default path var string is :{var_name}

        can be overwritten
        """
        baseurl = self.point.url
        for k, v in self.path.items():
            baseurl = baseurl.replace(f":{k}", str(v))
        self.url = urljoin(self.handler.base_url, baseurl)

    def execute(self) -> RequestResult:
        if self.check:
            self.check_and_finalize_value()

        self.handler.pre_request_callback(point=self.point, prep=self)
        # url
        self.prep_url()
        # request method
        self.prep_request_method()

        return self.execute_request(
            method=self.request_method, 
            url=self.url, 
            headers=self.headers, 
            body=self.body, 
            query=self.query
        )
    
    def execute_request(
            self, 
            method : typing.Callable, 
            url : str, 
            headers : dict, 
            body : dict, 
            query : dict
        )-> RequestResult:
        res = method(url=url, headers=headers, json=body, params=query)
        return self.result_target(res=res, handler=self.handler, point=self.point)
