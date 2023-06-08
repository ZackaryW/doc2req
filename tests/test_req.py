import os
import unittest
import orjson

from doc2req.model import  Api
from doc2req.req import Handler

class t_handler(unittest.TestCase):
    def setUp(self) -> None:
        with open("tests\\api_data.json", "rb") as f:
            data = orjson.loads(f.read())
        """        
        points = []
        for point_data in data:
            parameter = point_data.get("parameter")
            parameter_parsed = preprocess_dict(parameter)

            point = Point(**point_data)
            points.append(point)
        """
        self.api = Api(points=data)
        self.assertIsInstance(self.api, Api)

    def test_prep_iter(self):
        handler = Handler("https://habitica.com/",self.api)
        loginHelper =handler.prepReq("UserLoginLocal", username="test", password="test")
        for group, name, value, param in loginHelper.iter_all_fields():
            if name == "username":
                self.assertEqual(value, "test")
                self.assertEqual(param.field, "username")
                self.assertEqual(group, "body")
            else:
                self.assertEqual(value, "test")
                self.assertEqual(param.field, "password")
                self.assertEqual(group, "body")

    def test_handler(self):
        handler = Handler("https://habitica.com/",self.api)

        loginHelper =handler.prepReq(
            "UserLoginLocal", 
            username=os.environ["habi_username"], 
            password=os.environ["habi_password"]
        )
        
        result = loginHelper.execute()
        
        self.assertEqual(result.res.status_code, 200)