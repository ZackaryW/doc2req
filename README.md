# doc2req
doc2req is a library that simplfies the process of converting generated 
apidoc specifications into Python dataclasses (pydantic models) + other useful utilities.

## Key Features
1. convert apidoc specifications into pydantic models
2. generate request for each endpoint
3. generate apidoc specifications from source files dynamically

## Installation
```bash
pip install doc2req
```

## Usage

generate apidoc specifications from source files

```python
api : Api = from_src("src", clear_generated_node_modules=True)
```

access nodes
```python
api.points : List[Point]

# returns login point object by name
obj : Point | None = api["name::UserLoginLocal"] 

# returns login point object by url
obj : Point | None = api["url::/api/v3/user/login"]

# returns login point object by title
obj : Point | None = api["title::User Login"]

# returns first point object in group User
obj : Point | None = api["group::User"]
obj : Point | None = api["group::first::User"]

# returns last point object in group User
obj : Point | None = api["group::last::User"]

# returns all point objects in group User
obj : List[Point] | [] = api["group::all::User"]
```

point data structure
```python
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
```

create a request
```python
from doc2req.etc import UnpackableModel
class UserLogin(UnpackableModel):
    username : str
    password : str

    def unpack(self) -> dict:
        return {
            "username": self.username,
            "password": self.password
        }

test_login = UserLogin(username="xxxxx", password="xxxxx")

# create a request for login point
login :Point = api["name::UserLoginLocal"]
helper = login.prepReq(test_login)
result : RequestResult = helper.execute()

result.res : requests.Response

```
