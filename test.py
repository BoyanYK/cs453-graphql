from graphene.test import Client
import graph_schema

def test_hey():
    client = Client(graph_schema.get_schema())
    executed = client.execute('''{ hey }''', context={'user': 'Peter'})
    print(executed)
    assert executed == {
        'data': {
            'hey': 'hello Peter!'
        }
    }

test_hey()