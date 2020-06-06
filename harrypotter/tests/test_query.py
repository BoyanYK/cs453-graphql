from graphene.test import Client

from harrypotter.data import setup
from harrypotter.schema import schema


def test_hero_name_query():
    setup()
    client = Client(schema)
    query = """
        query HeroNameQuery {
          hero {
            name
          }
        }
    """
    print(client.execute(query))


def test_add_muggle():
    return None



test_hero_name_query()