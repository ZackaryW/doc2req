
import typing
from typing import Any

from pydantic import validator
from doc2req.etc.multi_model import MultiModel


class Parameter(MultiModel):
    group : str 
    type : str 
    optional : bool = False
    field : str = None
    isArray : bool = False
    description : str
    allowedValues : typing.List[str] = None
    defaultValue : typing.Any = None
    parentNode : dict = None

    def __init__(self, **data):
        super().__init__(**data)

    def check_value(self, value):
        return value    
    
    def __check_value(self, value):
        """
        hidden layer of check_value that 
        also checks for defaultValue, AllowedValues and isArray
        """
        func =self.__getattribute__("check_value", skip=True)
        
        if value is None and self.defaultValue is None and not self.optional:
            raise ValueError(
                f"Value {value} is None for {self.field} which is not optional"
            )
        
        if value is None and self.defaultValue is not None:
            return func(value)
        
        if self.allowedValues is not None and value not in self.allowedValues:
            raise ValueError(f"Value {value} not allowed for {self.field}")
        
        if self.isArray and not isinstance(value, list):
            raise ValueError(f"Value {value} is not a list for {self.field}")
    
        if not self.isArray and isinstance(value, list):
            raise ValueError(f"Value {value} is a list for {self.field}")

        func =self.__getattribute__("check_value", skip=True)
        return func(value)

    def __getattribute__(self, __name: str, skip: bool = False) -> Any:
        if __name != "check_value" or skip:
            return super().__getattribute__(__name)
        
        return self.__check_value

    @validator("group", pre=True)
    def _group_lower(cls, v :str):
        return v.lower()

    def __hash__(self):
        return hash(self.group + self.field or "unknown" + self.type)