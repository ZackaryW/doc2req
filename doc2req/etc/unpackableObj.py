from pydantic import BaseModel

class UnpackableObj:
    """
    UnpackableObj is a mixin class that adds unpack method
    """

    def unpack(self)->dict:
        """
        returns a dict representation of the object
        """
        pass

class UnpackableModel(BaseModel, UnpackableObj):
    def unpack(self):
        return self.dict()
    