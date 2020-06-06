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


def test_add_wizard_query():
    setup()
    client = Client(schema)
    params = {"someId": "3000"}
    query = """
          query FetchSomeIDQuery($someId: String!) {
            wizard(id: $someId) {
              name
              signatureSpell
            }
          }
      """

    mutate = """
      mutation myFirstMutation {
          createWizard(
              id: 3000,
              name: "Anthony",
              signatureSpell: "Disappeario"
              appearsIn: [ORDPHNX]) {
                  Wizard {
                    name
                    signatureSpell
                  }
              }

      }
      """
    print(client.execute(query, variables=params))
    print(client.execute(mutate))
    print(client.execute(query, variables=params))



# test_hero_name_query()
test_add_wizard_query()