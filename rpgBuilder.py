# -*- coding: utf-8 -*-
"""
Character Generator for 5th Edition Dungeons and Dragons (and someday any rpg).

@author: auto-nom
"""

import sys
import random

import rpgSystem as ds

# Load the necessary data into dictionaries
# rpgData, namesData, statsData = ds.load_data()


def easy_gen(name, race, role):
    """
    Automatically generates a character for a given name, race, and role.

    Does not check if inputted race and role are valid atm, may cause errors
    """
    p = ds.Character(name, race, role)
    sList = ds.stat_roll()
    p.setScorelist(sList)
    ds.auto_assign(p)
    ds.add_bonuses(p)
    print(p)
    ds.query_save(p)
    return p


def random_gen():
    """ Randomly generates a character."""
    race = random.choice(ds.rpgData["Races"])
    role = random.choice(ds.rpgData["Roles"])

    if race == "Half-Elf":
        name = random.choice(ds.namesData["Human_names"] +
                             ds.namesData["Elf_names"])
    else:
        race_names = race + "_names"
        name = random.choice(ds.namesData[race_names])

    Char = ds.Character(name, race, role)
    sList = ds.stat_roll()
    Char.setScorelist(sList)
    ds.auto_assign(Char)
    ds.add_bonuses(Char)

    return Char


def new_player():
    """ Allows a user to generate a new character, step by step."""
    race = ds.race_gen()
    role = ds.role_gen()
    name = ds.name_gen(race)

    player1 = ds.Character(name, race, role)
    sList = ds.stat_gen()
    sList.sort(reverse=True)
    player1.setScorelist(sList)
    ds.score_assignment(player1)
    ds.modifier_assign(player1)

    return player1


# ---------------------------------------------------------------------------
def startCheck():
    if len(sys.argv) != 2:
        print('Usage: python rpgBuilder.py "random"',
              'or python rpgBuilder.py "new"')
        return 1
    else:
        if sys.argv[1] == "random":
            randumb = random_gen()
            print(randumb)
            ds.query_save(randumb)
            return 0
        elif sys.argv[1] == "new":
            newb = new_player()
            print(newb)
            ds.query_save(newb)
            return 0
        else:
            print('Usage: python rpgBuilder.py "random"',
                  'or python rpgBuilder.py "new"')
            return 1

if __name__ == '__main__':
    startCheck()
