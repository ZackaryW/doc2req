
from functools import cached_property
import typing
from pydantic import BaseModel, Field, validator
from doc2req.model.ret import Return
from doc2req.model.example import Example

from doc2req.model.parameter import Parameter
from doc2req.util import preprocess_dict

class Point(BaseModel):
    name : str
    type : typing.Literal["post", "get", "put", "delete", "patch"]
    url : str
    title : str
    description : str = None
    group : str
    parameter : typing.List[Parameter] = Field(default_factory=list)
    error : typing.List[Return] = None
    version : str = None
    filename : str = None
    groupTitle : str = None
    examples : typing.List[Example] = None
    success : typing.List[Return] = None

    class Config:
        keep_untouched = (cached_property,)

    @validator("type", pre=True)
    def _type_to_lower(cls, v :str):
        return v.lower()
    
    @validator("parameter", pre=True)
    def _parameter_to_list(cls,v :dict):
        ret =preprocess_dict(v)
        for item in ret:
            if "type" not in item:
                item["type"] = "String"
        return ret

    @validator("examples", pre=True)
    def _examples_to_list(cls,v :dict):
        ret =preprocess_dict(v)
        return ret

    @validator("error", pre=True)
    def _error_to_list(cls,v :dict):
        ret =preprocess_dict(v)
        return ret

    @validator("success", pre=True)
    def _success_to_list(cls,v :dict):
        ret =preprocess_dict(v)
        return ret
        
    @cached_property
    def mandatory_vars(self) -> typing.Dict[str, Parameter]:
        if self.parameter is None:
            return {}
        return {
            v.field : v for v in self.parameter if v.optional is False
        }

    @cached_property
    def all_vars(
       self
    ) -> typing.Dict[str, Parameter]:
        if self.parameter is None:
            return {}
        return {
            v.field : v for v in self.parameter
        }

    def iter_param(self, iter_type : typing.Literal["all", "mandatory", "optional"] = "all"):
        if self.parameter is None:
            return
        for param in self.parameter:
            if iter_type == "mandatory" and param.optional:
                continue
                
            if iter_type == "optional" and not param.optional:
                continue

            yield param.field, param

    def __getitem__(self, key :str):
        match key:
            case str() if key.startswith("param::") and (index:=key.split("::")[1]).isdigit():
                if self.parameter is None:
                    raise KeyError(f"parameter is None for {self.name}")
                return self.parameter[int(index)]
            case str() if key.startswith("error::") and (index:=key.split("::")[1]).isdigit():
                if self.error is None:
                    raise KeyError(f"error is None for {self.name}")
                return self.error[int(index)]
            case str() if key.startswith("success::") and (index:=key.split("::")[1]).isdigit():
                if self.success is None:
                    raise KeyError(f"success is None for {self.name}")
                return self.success[int(index)]
            case str() if key.startswith("example::") and (index:=key.split("::")[1]).isdigit():
                if self.examples is None:
                    raise KeyError(f"examples is None for {self.name}")
                return self.examples[int(index)]
            case str() if key.startswith("param::"):
                if self.parameter is None:
                    raise KeyError(f"parameter is None for {self.name}")
                for field, param in self.iter_param():
                    if field == key.split("::")[1]:
                        return param
            case str():
                if self.parameter is None:
                    raise KeyError(f"parameter is None for {self.name}")
                for field, param in self.iter_param():
                    if field == key:
                        return param
            case _:
                raise KeyError(f"Key {key} not found")
            
    def get(self, key : str, default= None):
        try:
            return self[key]
        except KeyError:
            return default