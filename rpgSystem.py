# -*- coding: utf-8 -*-
"""
Functions for character generation, and the Character class, for an rpg.
(Only really works for 5th Edition D&D at the moment)

@author: auto-nom
"""

import random
import json


def dice(sides, num=1):
    """ Rolls num dice with a specified number of sides."""
    total = 0
    for i in range(num):
        total += random.randint(1, sides)
    return total


def d20():
    """ Rolls a 20 sided dice with crit success and crit fail print-outs."""
    roll = random.randint(1, 20)
    if roll == 20:
        print("CRITICAL SUCCESS!")
    if roll == 1:
        print("CRITICAL FAILURE!")
    return roll


def load_data():
    """ Loads the various data files needed for the program."""
    with open("DATA/rpgData.json", 'r') as rpgd:
        rpgData = json.load(rpgd)

    with open("DATA/namesData.json", 'r') as rpgn:
        namesData = json.load(rpgn)

    with open("DATA/statsData.json", 'r') as rpgs:
        statsData = json.load(rpgs)

    return rpgData, namesData, statsData


# Load the data so it can be used in this file
rpgData, namesData, statsData = load_data()
# Create individual lists/dictionaries from data
try:
    Attributes = rpgData["Attributes"]
    Races = rpgData["Races"]
    Roles = rpgData["Roles"]
except KeyError as err:
    print("DATA/rpgDATA.json is missing a", str(err), "section")
    raise

try:
    RaceStats = statsData["RaceStats"]
    RoleStats = statsData["RoleStats"]
except KeyError as err:
    print("DATA/statsData/json is missing a", str(err), "section")
    raise


# ---------------------------------------------------------------------------
class Character(object):
    """
    A character usable in Dungeons and Dragons 5th edition.

    Has a race and class, as well ability scores and stats.
    """

    def __init__(self, name, race, role):

        self.name = name
        self.race = race
        self.role = role

        self.hitpoints = 0

        self.attribDict = {}

        for i in Attributes:
            self.attribDict[i] = 0

        self.scorelist = []

    def calc_mod(self, stat):
        """
        Calculates ability modifiers for a given ability.

        Input: an ability score.
        Output: the modifier for that ability.
        """
        modifier = (stat - 10) // 2
        return modifier

    # Get attributes
    def getName(self):
        return self.name

    def getRace(self):
        return self.race

    def getRole(self):
        return self.role

    def getAttrib(self, attribute):
        try:
            return self.attribDict[attribute]
        except KeyError as err:
            print("Error: This character has no", str(err), "attribute")
            return False

    def getAttribDict(self):
        return self.attribDict.copy()

    def getHitpoints(self):
        return self.hitpoints

    def getScorelist(self):
        return self.scorelist.copy()

    # Set attributes
    def setName(self, X):
        self.name = X

    def setRace(self, X):
        self.race = X

    def setRole(self, X):
        self.role = X

    def setAttrib(self, attribute, X):
        self.attribDict[attribute] = X

    def setHitpoints(self, X):
        self.hitpoints = X

    def setScorelist(self, X):
        """ X is a list of integers."""
        self.scorelist = X

    def saveChar(self, filename="default"):
        """
        Save a Character into a json object.

        filename will default to the character's name if no argument is given.
        """
        if filename == "default":
            filename = self.name

        # Dictionary to create json object
        charDict = {
                    "Name": self.name,
                    "Race": self.race,
                    "Role": self.role,
                    "Attributes": self.attribDict,
                    "Hitpoints": self.hitpoints
                    }

        try:
            with open(filename, 'x') as f:
                json.dump(charDict, f, sort_keys=True, indent=4)
                print("Save successful")
        except FileExistsError:
            while True:
                print("The file", str(filename),
                      "already exists, do you want to overwrite it?")
                print("Yes to overwrite or No to abort")
                overwrite = input(">")
                overwrite = overwrite.upper()
                if overwrite == "Y" or overwrite == "YES":
                    with open(filename, 'w') as f:
                        json.dump(charDict, f, sort_keys=True, indent=4)
                        print("Save successful")
                        break
                elif overwrite == "N" or overwrite == "NO":
                    print("Saving process aborted")
                    break
                else:
                    print("Invalid command")

    def __str__(self):
        return("Name: {self.name}\n"
               "Race: {self.race}\n"
               "Class: {self.role}\n".format(self=self) +
               "\n".join(
                   "{}: {}".format(k, v) for k, v in self.attribDict.items()) +
               "\nHitpoints: {self.hitpoints}".format(self=self))


# ---------------------------------------------------------------------------
def load_char(filename):
    """ Loads a Character from a json object."""
    try:
        with open(filename, 'r') as savefile:
            charDict = json.load(savefile)
    except FileNotFoundError:
        print("That file could not be found :(")
        return

    savedChar = Character(charDict["Name"], charDict["Race"], charDict["Role"])

    for i in charDict["Attributes"]:
        savedChar.setAttrib(i, charDict["Attributes"][i])
    savedChar.setHitpoints(charDict["Hitpoints"])

    print("Character", str(savedChar.getName()), "sucessfully loaded")
    return savedChar


def query_save(player):
    """ Ask whether to save a Character or not."""
    while True:
        print("Do you want to save this character?")
        print("Yes to save or No to continue without saving")
        conf = input(">")
        conf = conf.upper()
        if conf == "Y" or conf == "YES":
            print("Enter a name for this save",
                  "or 'default' to use the character's name")
            filename = input(">")
            print("Saving...")
            player.saveChar(filename)
            break
        elif conf == "N" or conf == "NO":
            print("Character not saved")
            break
        else:
            print("Invalid command")


def stat_roll():
    """
    Rolls ability scores.

    Output: a list of scores in descending order,
    which can then be assigned to abilities.
    """
    scorelist = []
    for i in range(len(Attributes)):
        statlist = []
        for j in range(4):
            statlist.append(dice(6))
        statlist.remove(min(statlist))

        ability_score = 0
        for num in statlist:
            ability_score += num
        scorelist.append(ability_score)

    scorelist.sort(reverse=True)
    return scorelist


# ---------------------------------------------------------------------------
def race_gen():
    """ Race generation for a Character."""
    while True:
        print()
        print("What race do you want to play as?")
        print("You can choose from the following:", str(Races))
        print('Type "random" for a random race')
        race = input(">")
        race = race.title()        # .title works for Half-Elf etc.

        if race.lower() == "random":
            race = random.choice(Races)
            while True:
                print("Is a", str(race), "fine?")
                print("Type Yes to confirm, No to re-random",
                      "or X to pick for yourself")
                confirm = input(">")
                confirm = confirm.upper()
                if confirm == "Y" or confirm == "YES":
                    print("You are a", str(race) + "!")
                    return race
                elif confirm == "X":
                    race = "X"
                    break
                elif confirm == "N" or confirm == "NO":
                    race = random.choice(Races)
                else:
                    print("Invalid command")

        # Avoid "Invalid selection" printout if the user decides to repick
        if race == "X":
            pass

        elif race not in Races:
            print("Invalid selection\n")

        else:
            if race[0] in ['A', 'E', 'I', 'O', 'U']:
                print("You are an", str(race) + "!")
                return race
            else:
                print("You are a", str(race) + "!")
                return race


def role_gen():
    """
    Role generation for a Character.

    The term 'role' is instead of 'class' to be less confusing in the code.
    """
    while True:
        print()
        print("What class do you want to play as?")
        print("You can choose from the following:", str(Roles))
        print('Type "random" for a random class')
        role = input(">")
        role = role.capitalize()

        if role.lower() == "random":
            role = random.choice(Roles)
            while True:
                print("Is a", str(role), "fine?")
                print("Type Yes to confirm, No to re-random",
                      "or X to pick for yourself")
                confirm = input(">")
                confirm = confirm.upper()
                if confirm == "Y" or confirm == "YES":
                    print("You are a", str(role) + "!")
                    return role
                elif confirm == "X":
                    role = "X"
                    break
                elif confirm == "N" or confirm == "NO":
                    role = random.choice(Roles)
                else:
                    print("Invalid command")

        # Avoid the "Invalid selection" printout if the user decides to repick
        if role == "X":
            pass

        elif role not in Roles:
            print("Invalid selection\n")

        else:
            if role[0] in ['A', 'E', 'I', 'O', 'U']:
                print("You are an", str(role) + "!")
                return role
            else:
                print("You are a", str(role) + "!")
                return role


def name_gen(race):
    """ Name generation."""
    while True:
        print()
        print("What do you want your character to be named")
        print('Input your name now,',
              'or type "random" for a random name based on your race')
        name = input(">")

        if name.lower() == "random":
            # Half-Elves don't have their own specific names
            # Need to make this non-hardcoded; put in the data files somehow
            # Easiest would be copy paste elf+human names into Half-Elf_names
            if race == "Half-Elf":
                name = random.choice(namesData["Human_names"] +
                                     namesData["Elf_names"])

            else:
                race_names = race + "_names"
                try:
                    name = random.choice(namesData[race_names])
                except KeyError:
                    name = random.choice(namesData["Common_Names"])

        print("You are named:", str(name) + "!")
        return name


def points_mode():
    """ Manually generate ability scores using the points mode."""
    pDict = {}
    # json changes dict keys to strings even if they were originally integers
    try:
        for i in statsData["PointsCost"]:
            pDict[int(i)] = statsData["PointsCost"][i]
        points = statsData["PointsTotal"]
    except KeyError as err:
        print("DATA/statsData does not have a", str(err), "section")
        return False

    print("You have", str(points), "points to spend")
    print("The ability score to point cost is as follows:\n" + str(pDict))
    sList = []
    for i in range(len(Attributes)):
        sList.append(min(pDict))
    print("Your current scorelist is:", str(sList))

    while True:
        print("You have", str(points), "points left,",
              "do you want to leave your scores as they are and continue,"
              "or do you want to change your scores by using those points?")
        print("Type 'Edit' to change your scores,",
              "or 'Continue' to leave them as they are and continue")
        conf = input(">")
        conf = conf.upper()
        if conf == "C" or conf == "CONTINUE":
            return sList
        elif conf == "E" or conf == "EDIT":
            print("Your current scorelist is:", str(sList))
            print("Which score do you want to change?")
            print("Enter the number of the score to change",
                  "(A number between 1 and 6), or Back to go back")
            sIndex = input(">")
            if sIndex.upper() == "B" or sIndex.upper() == "BACK":
                pass
            else:
                try:
                    sIndex = int(sIndex) - 1
                except ValueError:
                    print("You must enter a number")
                else:
                    if sIndex < 0 or sIndex > 5:
                        print("You must enter a number between 1 and 6")
                    else:
                        print("What do you want to change this score to?")
                        valid = False
                        while not valid:
                            print("Enter a number between 8 and 15,",
                                  "that you have enough points for,",
                                  "or Back to go back")
                            scoreI = input(">")
                            if (scoreI.upper() == "B" or
                                    scoreI.upper() == "BACK"):
                                valid = True
                            else:
                                # such indent, much wow
                                try:
                                    scoreI = int(scoreI)
                                except ValueError:
                                    print("You must enter a number")
                                else:
                                    if scoreI < min(pDict):
                                        print("You are not allowed a score",
                                              "less than", str(min(pDict)),
                                              "with this method")
                                    elif scoreI > max(pDict):
                                        print("You are not allowed a score",
                                              "greater than", str(max(pDict)),
                                              "with this method")
                                    elif (points - (pDict[scoreI] -
                                                    pDict[sList[sIndex]]) < 0):
                                        print("You have insufficient points",
                                              "for this score")
                                    else:
                                        points -= (pDict[scoreI] -
                                                   pDict[sList[sIndex]])
                                        sList[sIndex] = scoreI
                                        valid = True
        else:
            print("Invalid command")


def stat_gen():
    """ Generate ability scores using whatever mode is chosen."""
    try:
        StandardPoints = statsData["StandardPoints"]
    except KeyError:
        StandardPoints = False
    while True:
        print()
        print("Do you want to generate your stats by die rolling,",
              "the point buy system, or take the standard scores if there are")
        print("This step is just generating the list of scores, you will",
              "assign them to the stats you choose in the following step")
        print('Type "dice" to have them randomly generated for you,',
              'or "points" to use the point buy system,')
        if StandardPoints:
            print('or type "standard" to get the scores', str(StandardPoints))
        stat_mode = input(">")
        stat_mode = stat_mode.lower()
        # standard only applies if it has been set in statsData
        if stat_mode == "standard":
            if not StandardPoints:
                print("A set of standard points have not been set in",
                      "DATA/statsData.json")
            else:
                sList = StandardPoints
                print("Your stats are:", str(sList))
                return sList

        elif stat_mode == "dice":
            rerolls = 2
            sList = stat_roll()
            while rerolls >= 0:
                print("Your stats are:", str(sList))
                if rerolls > 0:
                    print("Do you want to keep these or reroll?", str(rerolls),
                          "rerolls remaining")
                    print("Type Yes to keep or No to reroll")
                    conf = input(">")
                    conf = conf.upper()
                    if conf == "Y" or conf == "YES":
                        return sList
                    elif conf == "N" or conf == "NO":
                        rerolls -= 1
                        sList = stat_roll()
                    else:
                        print("Invalid command")
                else:
                    print("You are out of rerolls,",
                          "so I guess you're keeping those :P")
                    return sList

        elif stat_mode == "points":
            return points_mode()

        else:
            print("Invalid command")


def modifier_assign(player):
    """
    Assigns modifiers from attributes

    (just hitpoints for now actually)
    """
    const = player.getAttrib("Constitution")
    if const is False:        # Saying not const would be True if const was 0
        print("HP cannot be calculated without a Constitution attribute")
        return False
    try:
        hp = (RoleStats[player.role]["HitpointsBase"] +
              player.calc_mod(const))
    except KeyError as err:
        print("Error:", str(err), "not found in RoleStats section of",
              "DATA/statsData.json file")
        return False

    player.setHitpoints(hp)


def auto_assign(player):
    """ Assigns the character's ability scores based on its class."""
    for i in Attributes:
        prio = i + "Priority"
        try:
            player.setAttrib(i, player.scorelist[RoleStats[player.role][prio]])
        except KeyError as err:
            print("Error:", str(err), "not found in RoleStats section of",
                  "DATA/statsData.json file")
            return False

        except IndexError as err:
            print(str(prio), "in DATA/statsData.json does not refer to a",
                  "valid scorelist index. Refer to readme for how this works")

    modifier_assign(player)


def add_bonuses(player):
    """ Bases the character's bonuses on its race. """

    for i in Attributes:
        bonus = i + "Bonus"
        current = player.getAttrib(i)
        if current is False:
            # getAttrib will have printed out error message and returned False
            print("Unable to add", str(i), "bonus")

        else:
            try:
                val = (current + RaceStats[player.race][bonus])
            except KeyError as err:
                print("Error:", str(err), "not found in RaceStats section of",
                      "DATA/statsData.json file")
                return False

            player.setAttrib(i, val)

    # Half-Elves get +1 to 2 scores, randomly chosen for now
    # Need to make this non-hardcoded; put in the data files somehow
    if player.race == "Half-Elf":

        a = random.choice(Attributes)
        val = player.getAttrib(a) + 1
        player.setAttrib(a, val)

        b = random.choice(Attributes)
        player.getAttrib(b) + 1
        player.setAttrib(b, val)


def score_assignment(player):
    """ Assignment of scores from scorelist to abilities."""
    while True:
        print()
        print("Do you want to manually assign the scores generated",
              "in the previous step to your attributes,",
              "or do you want them to be automatically assigned",
              "as best fits your class?")
        print("Type Yes for manual assignment or No for automatic assignment")
        assign_mode = input(">")
        assign_mode = assign_mode.upper()
        if assign_mode == "N" or assign_mode == "NO":
            auto_assign(player)
            break

        elif assign_mode == "Y" or assign_mode == "YES":
            sList = player.getScorelist()
            sListCopy = sList.copy()
            abilityCopy = Attributes.copy()

            while True:
                print("Your scores to assign are:", str(sListCopy))
                i = sListCopy[0]
                print("What attribut to you want to be", str(i) + "?")
                print("Choose from", str(abilityCopy))
                abil = input(">")
                abil = abil.capitalize()
                if abil not in abilityCopy:
                    print("That attribute is not available")

                else:
                    player.setAttrib(abil, i)

                    abilityCopy.remove(abil)
                    sListCopy.remove(i)

                if sListCopy == []:
                    break

            add_bonuses(player)
            break

        else:
            print("Invalid input")
