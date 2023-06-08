import unittest
import orjson

from doc2req.model import Point , Api
from doc2req.model.parameter import Parameter
from doc2req.util import preprocess_dict

class t_model(unittest.TestCase):
    def test_api(self):
        with open("tests\\api_data.json", "rb") as f:
            data = orjson.loads(f.read())
        for point_data in data:
            example_raw = point_data.get("examples",{})
            example_parsed = preprocess_dict(example_raw)
            self.assertIsInstance(example_parsed, list)
            
            parameter_raw = point_data.get("parameter",{})
            parameter_parsed = preprocess_dict(parameter_raw)
            self.assertIsInstance(parameter_parsed, list)

            point = Point(**point_data)
            self.assertIsInstance(point, Point)

        api = Api(points=data)
        self.assertIsInstance(api, Api)
        return api
    
class t_model_2(unittest.TestCase):

    def setUp(self) -> None:
        with open("tests\\api_data.json", "rb") as f:
            data = orjson.loads(f.read())
        self.api = Api(points=data)

    def test_api_lookup1(self):
        """
        default by name checks
        """
        point = self.api.by_name("UserLoginLocal")
        self.assertIsInstance(point, Point)
        point = self.api["UserLoginLocal"]
        self.assertIsInstance(point, Point)

    def test_api_lookup2(self):
        """
        name:: checks
        """
        point = self.api["name::UserLoginLocal"]
        self.assertIsInstance(point, Point)
        self.assertEqual(point.name, "UserLoginLocal")

    def test_api_lookup3(self):
        """
        url:: and title:: checks
        """
        point = self.api["url::/api/v3/user/auth/local/login"]
        point2 = self.api["title::Login"]
        self.assertEqual(point, point2)

    def test_parameter_1(self):
        point = self.api["url::/api/v3/user/auth/local/login"]
        self.assertIsInstance(point["username"], Parameter)
        self.assertEqual(point["username"].type, "String")
        self.assertIsInstance(point["password"], Parameter)
        self.assertEqual(point["password"].type, "String")
