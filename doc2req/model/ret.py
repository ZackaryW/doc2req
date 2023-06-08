
from pydantic import BaseModel


class Return(BaseModel):
    group : str
    type : str = None
    optional : bool = False
    field : str = None
    isArray : bool = False
    description : str = None