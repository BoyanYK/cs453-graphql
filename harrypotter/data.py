wizard_data = {}
muggle_data = {}


def setup():
    from .schema import Wizard, Muggle

    global wizard_data, muggle_data
    harry = Wizard(
        id="1000",
        name="Harry Potter",
        friends=["1001", "1002", "1004", "1003"],
        appears_in=[5, 6, 7],
        signature_spell=['Expelliarmus'],
        primary_house=['Gryffindor']
    )

    hermione = Wizard(
        id="1001",
        name="Hermione Granger",
        friends=["1000", "1002", "1004"],
        appears_in=[5, 6, 7],
        signature_spell=['Alohomora'],
        primary_house=['Gryffindor']
    )

    # probably maxed stat wingardium leviosa
    # after incident with Hermione
    ron = Wizard(
        id="1002",
        name="Ronald Weasley",
        friends=["1000", "1001", "1004"],
        appears_in=[5, 6, 7],
        signature_spell=['Wingardium Leviosa'],
        primary_house=['Gryffindor']
    )

    voldemort = Wizard(
        id="1003",
        name="Tom Marvolo Riddle",
        friends=["1000", "1004"],
        appears_in=[5, 6, 7],
        signature_spell=['Expelliarmus'],
        primary_house=['Slytherin']
    )

    dumbledore = Wizard(
        id="1004",
        name="Albus Percival Wulfric Brian Dumbledore",
        friends=["1000", "1001", "1002", "1003"],
        appears_in=[5, 6, 7],
        signature_spell=['Apparation'],
        primary_house=['Gryffindor']
    )

    frank = Muggle(
        id="2000",
        name="Frank Bryce",
        friends=["1000", "10003"],
        appears_in=[6],
        magical_ability=False
    )

    dursley = Muggle(
        id="2001",
        name="Dudley Dursley",
        friends=["1001"],
        appears_in=[5, 6, 7],
        magical_ability=False
    )

    wizard_data = {
        "1000": harry,
        "1001": hermione,
        "1002": ron,
        "1003": voldemort,
        "1004": dumbledore,
    }

    muggle_data = {
        "2000": frank,
        "2001": dursley
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
