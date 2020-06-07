import graphene

from harrypotter.data import get_wizard, get_hero, get_muggle, add_wizard, add_muggle


class Book(graphene.Enum):
    ORDPHNX = 5
    HBPRNCE = 6
    DTHLWS = 7


class Character(graphene.Interface):
    id = graphene.ID()
    name = graphene.String()
    friends = graphene.List(lambda: Character)
    appears_in = graphene.List(Book)

    def resolve_friends(self, info):
        # The character friends is a list of strings
        return [get_wizard(f) for f in self.friends]
        return None


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


class Query(graphene.ObjectType):
    hero = graphene.Field(Character, book=Book())
    wizard = graphene.Field(Wizard, id=graphene.String())
    muggle = graphene.Field(Muggle, id=graphene.String())

    def resolve_hero(root, info, episode=None):
        return get_hero(episode)

    def resolve_wizard(root, info, id):
        return get_wizard(id)

    def resolve_muggle(root, info, id):
        return get_muggle(id)


class CreateWizard(graphene.Mutation):
    Wizard = graphene.Field(Wizard)

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        appears_in = graphene.List(Book)
        signature_spell = graphene.String()

    def mutate(self, info, id, name, appears_in, signature_spell):
        wizard = Wizard(id, name, appears_in, signature_spell)
        add_wizard(wizard)
        return CreateWizard(wizard)


class CreateMuggle(graphene.Mutation):
    Muggle = graphene.Field(Muggle)

    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        appears_in = graphene.List(Book)

    def mutate(self, info, id, name, appears_in):
        muggle = Muggle(id, name, appears_in)
        add_muggle(muggle)
        return CreateMuggle(muggle)


class Mutation(graphene.ObjectType):
    create_wizard = CreateWizard.Field()
    create_muggle = CreateMuggle.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
