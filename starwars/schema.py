import graphene

from starwars.data import get_character, get_droid, get_hero, get_human, add_human


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
        return get_hero(episode)

    def resolve_human(root, info, id):
        return get_human(id)

    def resolve_droid(root, info, id):
        return get_droid(id)


class CreateHuman(graphene.Mutation):
    human = graphene.Field(Human)

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        appears_in = graphene.List(Episode)

    def mutate(self, info, id, name, appears_in):
        human = Human(id, name, appears_in)
        add_human(human)
        return CreateHuman(human)


class Mutation(graphene.ObjectType):
    create_human = CreateHuman.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)