from graphene import ObjectType, String, Schema
import graphene

people = []
class Person(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int()

class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    person = graphene.Field(lambda: Person)

    def mutate(root, info, name):
        person = Person(name=name)
        people.append(person)
        ok = True
        return CreatePerson(person=person, ok=ok)

class MyMutations(graphene.ObjectType):
    create_person = CreatePerson.Field()

class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()
    person = graphene.Field(Person())

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'

    def resolve_person(root, info):
        return people[0]

# @staticmethod
def get_schema():
    schema = Schema(query=Query, mutation=MyMutations)
    return schema

query_string = '''mutation myFirstMutation {
    createPerson(name:"Peter") {
        person {
            name
        }
        ok
    }
}'''
schema = get_schema()
result = schema.execute(query_string)
print(result)
query_string = " { person }"
result = schema.execute(query_string)
print(result)