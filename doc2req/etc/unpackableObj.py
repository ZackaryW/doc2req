from pydantic import BaseModel

class UnpackableObj:
    def unpack(self):
        pass

class UnpackableModel(BaseModel, UnpackableObj):
    def unpack(self):
        return self.dict()
    