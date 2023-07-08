

from pydantic import BaseModel, VERSION

if VERSION.startswith("1."):
    from pydantic.main import ModelMetaclass
else:
    from pydantic._internal._model_construction import ModelMetaclass

class MultiModelMeta(ModelMetaclass):
    """
    # other keys
    __type_var__ : is a key to store the var name of the type
    """
    
    _base_cls = None
    _sub_classes = {}
    _parent_classes = {}

    def __new__(cls, name, bases, namespace, **kwargs):
        if cls._base_cls is None:
            cls._base_cls = super().__new__(cls, name, bases, namespace, **kwargs)
            return cls._base_cls
        
        # check if base is MultiModel
        parentMultiModel = None
    
        for base in bases:
            if issubclass(base, MultiModel):
                parentMultiModel = base
                break
        
        type_var = namespace.get("__type_var__", "type")
        namespace["__type_var__"] = type_var

        newcls : BaseModel = super().__new__(
            cls, name, bases, namespace, **kwargs
        )
        
        if parentMultiModel == MultiModel:
            return newcls
        
        if parentMultiModel not in cls._sub_classes:
            cls._sub_classes[parentMultiModel] = {}

        type_key = namespace.get(type_var, None)
        if type_key is not None:
            cls._sub_classes[parentMultiModel][type_key] = newcls
        cls._parent_classes[newcls] = parentMultiModel
        return newcls
    
    def __call__(cls, **kwargs):
        no_more = kwargs.pop("__no_xxx_more", False)
        if no_more:
            return super().__call__(**kwargs)

        type_var = getattr(cls, "__type_var__")
        type_key = kwargs.get(type_var, None)

        parentCls = cls._parent_classes.get(cls, cls)
        
        if parentCls not in cls._sub_classes:
            return parentCls(**kwargs, __no_xxx_more=True)

        targetCls = cls._sub_classes[parentCls].get(type_key, parentCls)

        
        return targetCls(**kwargs, __no_xxx_more=True)
    
        
class MultiModel(BaseModel, metaclass=MultiModelMeta):
    """
    MultiModel is a BaseModel that allows derivation of subclasses on creation

    ### Example:
    ```python
    class Ex0(MultiModel):
        # by default, type var is used to determine the subclass

    class Ex1(Ex0):
        type = "ex1"
    
    class Ex2(Ex0):
        type = "ex2"

    assert isinstance(Ex0(type="ex1"), Ex1)
    assert isinstance(Ex0(type="ex2"), Ex2)

    ```
    """
