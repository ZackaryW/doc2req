import unittest
from doc2req.model.api import Api

from doc2req.tool import from_src

class t_tool(unittest.TestCase):
    def test_gen_tool(self):
        x = from_src(
            "tests/habitica_src", 
            clear_generated_node_modules=True
        )
        self.assertIsInstance(x, Api)