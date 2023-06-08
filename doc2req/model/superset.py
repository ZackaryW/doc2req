

from doc2req.model.parameter import Parameter
from validate_email import validate_email
import uuid
class EmailParameter(Parameter):
    type :str = "email"

    def check_value(self, value):
        # check is email
        is_valid = validate_email(
            email_address=value,
            check_regex=True, 
        )

        if not is_valid:
            raise ValueError(f"invalid email address: {value}")
        
        return value
    
class UUIDParameter(Parameter):
    type :str = "uuid"

    def check_value(self, value):
        # check is uuid
        try:
            return uuid.UUID(value)
        except ValueError:
            raise ValueError(f"invalid uuid: {value}")
        

class StringParameter(Parameter):
    type :str = "String"

    def check_value(self, value):
        # check is string
        if not isinstance(value, str):
            raise ValueError(f"invalid string: {value}")
        
        return str(value)
    
class NumberParameter(Parameter):
    type :str = "Number"

    def check_value(self, value):
        # check is number
        if not isinstance(value, int):
            raise ValueError(f"invalid number: {value}")
        
        return int(value)

class StringArrayParameter(Parameter):
    type :str = "String[]"

    def check_value(self, value):
        # check is string
        if not isinstance(value, list):
            raise ValueError(f"invalid string array: {value}")
        
        return [str(v) for v in value]
    
class IntegerArrayParameter(Parameter):
    type :str = "Integer[]"

    def check_value(self, value):
        # check is string
        if not isinstance(value, list):
            raise ValueError(f"invalid integer array: {value}")
        
        return [int(v) for v in value]
    

    