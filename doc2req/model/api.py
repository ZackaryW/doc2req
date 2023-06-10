import typing
from pydantic import BaseModel
from doc2req.model.point import Point

class Api(BaseModel):
    """
    Api object is a collection of points

    supports rich __getitem__ methods

    ### examples:

    ```python
    api = Api(points=points)
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
    """

    points : typing.List[Point]

    def by_name(self, name :str):
        for point, cname in self.iter_field("name"):
            if name == cname:
                return point   

    def by_url(self, url :str):
        for point, curl in self.iter_field("url"):
            if url == curl:
                return point
        
    
    def by_title(self, title :str):
        for point, ctitle in self.iter_field("title"):
            if title == ctitle:
                return point
    
    def by_group(
            self,
            group :str, 
            return_type : typing.Literal["first", "last", "all"] = "first",
        ):
        points = []
        for point, cgroup in self.iter_field("group"):
            if group == cgroup:
                if return_type == "first":
                    return point
                points.append(point)
        if return_type == "last":
            return points[-1]
        return points

    def iter_fields(self, *fields):
        if len(fields) == 0:
            return
        
        if len(fields) == 1:
            for point in self.points:
                yield getattr(point, fields[0])

        for point in self.points:
            yield point, tuple(getattr(point, field) for field in fields)

    def iter_field(self, field):
        for point in self.points:
            if not hasattr(point, field):
                continue
            yield point, getattr(point, field)
        

    def __getitem__(self, key:str)-> typing.Union[Point, None]:
        match key:
            case str() if key.startswith("name::"):
                return self.by_name(key.split("::")[1])
            case str() if key.startswith("url::"):
                return self.by_url(key.split("::")[1])
            case str() if key.startswith("title::"):
                return self.by_title(key.split("::")[1])
            case str() if key.startswith("group::first::"):
                return self.by_group(key.split("::")[2], "first")
            case str() if key.startswith("group::last::"):
                return self.by_group(key.split("::")[2], "last")
            case str() if key.startswith("group::all::"):
                return self.by_group(key.split("::")[2], "all")
            case str() if key.startswith("group::"):
                return self.by_group(key.split("::")[1])
            case str():
                return self.by_name(key)
            case int():
                return self.points[key]
            case slice():
                return self.points[key]
            case Point():
                # return index
                for i, point in enumerate(self.points):
                    if point == key:
                        return i
                return None
            case _:
                raise KeyError(f"invalid key: {key}")
        
                

