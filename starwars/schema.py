import graphene
from graphql import GraphQLError

from .data import get_human_data, get_droid_data

class Episode(graphene.Enum):
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6


class Character(graphene.Interface):
    id = graphene.ID()
    name = graphene.String()
    friends = graphene.List(lambda: Character)
    appears_in = graphene.List(Episode)

    def resolve_friends(self, info):
        # The character friends is a list of strings
        
        return [get_character(f) for f in self.friends]

    def get_character(f):
        human_data = get_human_data()
        droid_data = get_droid_data()
        return human_data.get(id) or droid_data.get(id)

class Human(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    home_planet = graphene.String()


class Droid(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    primary_function = graphene.String()


class Query(graphene.ObjectType):
    hero = graphene.Field(Character, episode=Episode())
    human = graphene.Field(Human, id=graphene.String())
    droid = graphene.Field(Droid, id=graphene.String())

    

    def resolve_hero(root, info, episode=None):
        human_data = get_human_data()
        droid_data = get_droid_data()
        if episode == 5:
            return human_data["1000"]
        return droid_data["2001"]

    def resolve_human(root, info, id):
        human_data = get_human_data()
        if int(id) < 1000:
            return GraphQLError("Invalid ID")
        if human := human_data.get(id):
            return human
        else:
            return GraphQLError("User does not exist")

    def resolve_droid(root, info, id):
        droid_data = get_droid_data()
        if droid := droid_data.get(id):
            return droid
        else:
            raise GraphQLError("User does not exist")


class CreateHuman(graphene.Mutation):
    human = graphene.Field(Human)

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        appears_in = graphene.List(Episode)

    def mutate(self, info, id, name, appears_in):
        human_data = get_human_data()
        human = Human(id, name, appears_in)
        human_data[human.id] = human
        return CreateHuman(human)


class Mutation(graphene.ObjectType):
    create_human = CreateHuman.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)