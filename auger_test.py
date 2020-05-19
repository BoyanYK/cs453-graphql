# Test moved from the auto-generated place so that I could easily fixed the imports
# No other changes
import hello
from hello import Query
import __main__
import graphene
import graphene.types.schema
from graphene.types.schema import Schema
from mock import patch
import unittest


class HelloTest(unittest.TestCase):
    @patch.object(Schema, 'execute')
    @patch.object(Schema, '__init__')
    def test_main(self, mock___init__, mock_execute):
        mock___init__.return_value = None
        mock_execute.return_value = <graphql.execution.base.ExecutionResult object at 0x7fe763172d40>
        self.assertEqual(
            __main__.main(),
            None
        )


    def test_resolve_hello(self):
        self.assertEqual(
            Query.resolve_hello(self=None,info=<graphql.execution.base.ResolveInfo object at 0x7fe76315ca40>,name='World'),
            'Hello World'
        )


if __name__ == "__main__":
    unittest.main()
