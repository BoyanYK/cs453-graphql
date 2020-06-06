import graphene


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
        # return [get_character(f) for f in self.friends]
        return None


class Muggle(graphene.ObjectType):
    class Meta:
        interfaces = (Character,)

    magic_ability = graphene.Boolean


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

    def resolve_human(root, info, id):
        info.context['trace'] += [1, 2, 3]
        return get_human(id)

    def resolve_droid(root, info, id):
        return get_droid(id)
