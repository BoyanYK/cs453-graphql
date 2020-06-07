import graphene
from graphql import GraphQLError

import harrypotter
import starwars
from harrypotter.data import get_wizard, get_muggle, add_wizard, add_muggle
from starwars.data import get_character, get_droid, get_human, add_human


class ScType(graphene.Enum):
    HP = 2
    SW = 1


class Episode(graphene.Enum):
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6
    ORDPHNX = 55
    HBPRNCE = 66
    DTHLWS = 77


class Character(graphene.Interface):
    sctype = graphene.List(ScType)
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


class Muggle(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    magical_ability = graphene.Boolean()


# where should Lily Evans/Hermione Granger be placed...
class Wizard(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    signature_spell = graphene.String()
    primary_house = graphene.String()


class Char(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)


class Query(graphene.ObjectType):
    hero = graphene.Field(Character, episode=Episode(), scType=ScType())
    human = graphene.Field(Human, id=graphene.String())
    droid = graphene.Field(Droid, id=graphene.String())
    wizard = graphene.Field(Wizard, id=graphene.String())
    muggle = graphene.Field(Muggle, id=graphene.String())
    char = graphene.Field(Char, id=graphene.String())

    def resolve_hero(root, info, episode=None, scType=None):
        if scType == ScType.SW:
            return starwars.data.get_hero(episode)
        elif scType == ScType.HP:
            return harrypotter.data.get_hero(episode)

    def resolve_char(root, info, id):
        if int(id) < 1000:
            return GraphQLError("Invalid ID")
        elif 1000 <= int(id) < 2000:
            return get_human(id)
        elif 2000 <= int(id) < 3000:
            return get_droid(id)
        elif 3000 <= int(id) < 4000:
            return get_wizard(id)
        elif 4000 <= int(id) < 5000:
            return get_muggle(id)
        else:
            return GraphQLError("User does not exist")

    # def resolve_human(root, info, id):
    #     return get_human(id)
    #
    # def resolve_droid(root, info, id):
    #     return get_droid(id)
    #
    # def resolve_wizard(root, info, id):
    #     return get_wizard(id)
    #
    # def resolve_muggle(root, info, id):
    #     return get_muggle(id)


class CreateHuman(graphene.Mutation):
    human = graphene.Field(Human)

    class Arguments:
        sctype = graphene.List(ScType)
        id = graphene.ID()
        name = graphene.String()
        appears_in = graphene.List(Episode)

    def mutate(self, info,sctype, id, name, appears_in):
        # TODO to check for existing ID before mutate
        if 1000 <= int(id) < 2000:
            human = Human(sctype, id, name, appears_in, sctype)
            add_human(human)
            return CreateHuman(human)
        else:
            return GraphQLError("1000 >= id < 2000 for humans")


class CreateWizard(graphene.Mutation):
    Wizard = graphene.Field(Wizard)

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        appears_in = graphene.List(Episode)
        signature_spell = graphene.String()
        sctype = graphene.List(ScType)

    def mutate(self, info, id, name, appears_in, signature_spell):
        if 3000 >= int(id) < 4000:
            wizard = Wizard(id, name, appears_in, signature_spell)
            add_wizard(wizard)
            return CreateWizard(wizard)
        else:
            return GraphQLError("1000 >= id < 2000 for humans")


class CreateMuggle(graphene.Mutation):
    Muggle = graphene.Field(Muggle)

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        appears_in = graphene.List(Episode)
        sctype = graphene.List(ScType)

    def mutate(self, info, id, name, appears_in):
        if 4000 >= int(id) < 5000:
            muggle = Muggle(id, name, appears_in)
            add_muggle(muggle)
            return CreateMuggle(muggle)
        else:
            return GraphQLError("1000 >= id < 2000 for humans")


class Mutation(graphene.ObjectType):
    create_human = CreateHuman.Field()
    create_wizard = CreateWizard.Field()
    create_muggle = CreateMuggle.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
