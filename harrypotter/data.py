wizard_data = {}
muggle_data = {}


def setup():
    from .schema import Wizard, Muggle

    global wizard_data, muggle_data
    harry = Wizard(
        id="3000",
        name="Harry Potter",
        friends=["3001", "3002", "3004", "3003", "4001"],
        appears_in=[55, 66, 77],
        signature_spell=['Expelliarmus'],
        primary_house=['Gryffindor']
    )

    hermione = Wizard(
        id="3001",
        name="Hermione Granger",
        friends=["3000", "3002", "3004"],
        appears_in=[55, 66, 77],
        signature_spell=['Alohomora'],
        primary_house=['Gryffindor']
    )

    # probably maxed stat wingardium leviosa
    # after incident with Hermione
    ron = Wizard(
        id="3002",
        name="Ronald Weasley",
        friends=["3000", "3001", "3004"],
        appears_in=[55, 66, 77],
        signature_spell=['Wingardium Leviosa'],
        primary_house=['Gryffindor']
    )

    voldemort = Wizard(
        id="1003",
        name="Tom Marvolo Riddle",
        friends=["3000", "3004"],
        appears_in=[55, 66, 77],
        signature_spell=['Expelliarmus'],
        primary_house=['Slytherin']
    )

    dumbledore = Wizard(
        id="3004",
        name="Albus Percival Wulfric Brian Dumbledore",
        friends=["3000", "3001", "3002", "3003"],
        appears_in=[55, 66, 77],
        signature_spell=['Apparation'],
        primary_house=['Gryffindor']
    )

    frank = Muggle(
        id="4000",
        name="Frank Bryce",
        friends=["3000", "3003"],
        appears_in=[66],
        magical_ability=False
    )

    dursley = Muggle(
        id="4001",
        name="Dudley Dursley",
        friends=["3001"],
        appears_in=[55, 66, 77],
        magical_ability=False
    )

    wizard_data = {
        "3000": harry,
        "3001": hermione,
        "3002": ron,
        "3003": voldemort,
        "3004": dumbledore,
    }

    muggle_data = {
        "4000": frank,
        "4001": dursley
    }


def get_character(id):
    return wizard_data.get(id) or muggle_data.get(id)


def add_wizard(wizard):
    wizard_data[wizard.id] = wizard


def add_muggle(muggle):
    muggle_data[muggle.id] = muggle


def get_friends(character):
    return map(get_character, character.friends)


def get_hero(book):
    if book in [5, 6, 7]:
        return wizard_data["1000"]
    return muggle_data["2001"]


def get_wizard(id):
    return wizard_data.get(id)


def get_muggle(id):
    return muggle_data.get(id)


def get_char_traits(id):
    return None
