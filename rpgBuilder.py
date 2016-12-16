#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Character Generator for 5th Edition Dungeons and Dragons (and someday any rpg).

@author: auto-nom
"""

import sys
import random

import rpgSystem as rs


def easy_gen(name, race, role, background):
    """
    Automatically generates a character for a given name, race, and role.

    Does not check if inputted race and role are valid atm, may cause errors
    """
    p = rs.Character(name, race, role, background)
    sList = rs.stat_roll()
    p.setScorelist(sList)
    rs.auto_assign(p)
    rs.add_bonuses(p)
    rs.modifier_assign(p)
    print(p)
    rs.query_save(p)
    return p


def random_gen():
    """ Randomly generates a character."""
    race = random.choice(rs.rpgData["Races"])
    role = random.choice(rs.rpgData["Roles"])
    background = random.choice(rs.rpgData["Backgrounds"])

    names = []
    majorRace = rs.RaceStats[race]["majorRace"]
    for i in majorRace:
        try:
            names += rs.namesData[i + "_names"]
        except KeyError:
            names += rs.namesData["Common_names"]

    name = random.choice(names)

    Char = rs.Character(name, race, role, background)
    sList = rs.stat_roll()
    Char.setScorelist(sList)
    rs.auto_assign(Char)
    rs.add_bonuses(Char)
    rs.modifier_assign(Char)

    return Char


def new_player():
    """ Allows a user to generate a new character, step by step."""
    race = rs.race_gen()
    role = rs.role_gen()
    # TODO: rs.background_gen()
    name = rs.name_gen(race)

    player1 = rs.Character(name, race, role)
    sList = rs.stat_gen()
    sList.sort(reverse=True)
    player1.setScorelist(sList)
    rs.score_assignment(player1)
    rs.modifier_assign(player1)

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
            rs.query_save(randumb)
            return 0
        elif sys.argv[1] == "new":
            newb = new_player()
            print(newb)
            rs.query_save(newb)
            return 0
        else:
            print('Usage: python rpgBuilder.py "random"',
                  'or python rpgBuilder.py "new"')
            return 1

if __name__ == '__main__':
    startCheck()
