
from pydantic import BaseModel


class Example(BaseModel):
    title: str
    content: str
    type : str = "json"
    