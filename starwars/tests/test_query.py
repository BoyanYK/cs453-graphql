from graphene.test import Client

from starwars.data import setup
from starwars.schema import schema


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

def test_hero_name_and_friends_query():
    setup()
    client = Client(schema)
    query = """
        query HeroNameAndFriendsQuery {
          hero {
            id
            name
            friends {
              name
            }
          }
        }
    """
    client.execute(query)

def test_nested_query():
    setup()
    client = Client(schema)
    query = """
        query NestedQuery {
          hero {
            name
            friends {
              name
              appearsIn
              friends {
                name
              }
            }
          }
        }
    """
    client.execute(query)


def test_fetch_luke_query():
    setup()
    client = Client(schema)
    query = """
        query FetchLukeQuery {
          human(id: "1000") {
            name
          }
        }
    """
    client.execute(query)

def test_fetch_id_query_mutate_query():
  setup()
  client = Client(schema)
  query = """
      query FetchSomeIDQuery($someId: String!) {
        human(id: $someId) {
          name
        }
      }
  """
  params = {"someId": "3000"}
  mutate = """
  mutation myFirstMutation {
      createHuman(
          id: 3000,
          name: "Anthony",
          appearsIn: []) {
              human {
                name
              }
          }
      
  }
  """
  print(client.execute(query, variables=params))
  print(client.execute(mutate))
  print(client.execute(query, variables=params))

def test_fetch_id_query_persistence():
  setup()
  client = Client(schema)
  query = """
      query FetchSomeIDQuery($someId: String!) {
        human(id: $someId) {
          name
        }
      }
  """
  params = {"someId": "3000"}
  con = {"trace": []}
  result = schema.execute(query, context=con)
  # con is updated here

# * Running these two tests consecutively should result in the first one querying, 
# * getting no data, then mutating and getting data on the second query
# * Then, the second test queries for the same data but as its a new instance, it gets no results (no persistence)
# test_fetch_id_query_mutate_query()
test_fetch_id_query_persistence()
# test_hero_name_query()

def test_fetch_some_id_query2():
    query = """
        query FetchSomeIDQuery($someId: String!) {
          human(id: $someId) {
            name
          }
        }
    """
    params = {"someId": "1002"}


def test_invalid_id_query():
    query = """
        query humanQuery($id: String!) {
          human(id: $id) {
            name
          }
        }
    """
    params = {"id": "not a valid id"}


def test_fetch_luke_aliased():
    query = """
        query FetchLukeAliased {
          luke: human(id: "1000") {
            name
          }
        }
    """


def test_fetch_luke_and_leia_aliased():
    query = """
        query FetchLukeAndLeiaAliased {
          luke: human(id: "1000") {
            name
          }
          leia: human(id: "1003") {
            name
          }
        }
    """


def test_duplicate_fields():
    query = """
        query DuplicateFields {
          luke: human(id: "1000") {
            name
            homePlanet
          }
          leia: human(id: "1003") {
            name
            homePlanet
          }
        }
    """


def test_use_fragment():
    query = """
        query UseFragment {
          luke: human(id: "1000") {
            ...HumanFragment
          }
          leia: human(id: "1003") {
            ...HumanFragment
          }
        }
        fragment HumanFragment on Human {
          name
          homePlanet
        }
    """


def test_check_type_of_r2():
    query = """
        query CheckTypeOfR2 {
          hero {
            __typename
            name
          }
        }
    """


def test_check_type_of_luke():
    query = """
        query CheckTypeOfLuke {
          hero(episode: EMPIRE) {
            __typename
            name
          }
        }
    """