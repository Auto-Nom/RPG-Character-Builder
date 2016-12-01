# -*- coding: utf-8 -*-
"""
Functions for character generation, and the Character class, for an rpg.
(Only really works for 5th Edition D&D at the moment)

@author: auto-nom
"""

import random
import json


def dice(sides, num=1):
    """ Rolls num dice with a specified number of sides. """
    total = 0
    for i in range(num):
        total += random.randint(1, sides)
    return total

def d20():
    """ Rolls a 20 sided dice with crit success and crit fail print-outs. """
    roll = random.randint(1,20)
    if roll == 20:
        print("CRITICAL SUCCESS!")
    if roll == 1:
        print("CRITICAL FAILURE!")
    return roll


def load_data():
    """ Loads the various data files needed for the program. """
    with open("rpgSystem.txt", 'r') as rpgs:
        rpgSystem = json.load(rpgs)
    
    with open("rpgNames.txt", 'r') as rpgn:
        rpgNames = json.load(rpgn)
    
    with open("rpgStats.txt", 'r') as rpgt:
        rpgStats = json.load(rpgt)

    return rpgSystem, rpgNames, rpgStats


# Load the data so it can be used in this file
# This line won't necessarily stay here but for now it's useful for testing
rpgSystem, rpgNames, rpgStats = load_data()

#----------------------------------------------------------------------------
class Character(object):
    """
    A character usable in Dungeons and Dragons 5th edition.
    
    Has a race and class, as well ability scores and stats.
    """
    
    def __init__(self, name, race, role):
        
        self.name = name
        self.race = race
        self.role = role
        
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0
        self.hitpoints = 0
        
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
        
    def getStrength(self):
        return self.strength
        
    def getDexterity(self):
        return self.dexterity
        
    def getConstitution(self):
        return self.constitution
        
    def getIntelligence(self):
        return self.intelligence
        
    def getWisdom(self):
        return self.wisdom
        
    def getCharisma(self):
        return self.charisma
        
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
        
    def setStrength(self, X):
        self.strength = X
        
    def setDexterity(self, X):
        self.dexterity = X
        
    def setConstitution(self, X):
        self.constitution = X
        
    def setIntelligence(self, X):
        self.intelligence = X
        
    def setWisdom(self, X):
        self.wisdom = X
        
    def setCharisma(self, X):
        self.charisma = X
        
    def setHitpoints(self, X):
        self.hitpoints = X
        
    def setScorelist(self, X):
        """ X is a list of 6 integers. """
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
        "Strength": self.strength,
        "Dexterity": self.dexterity,
        "Constitution": self.constitution,
        "Intelligence": self.intelligence,
        "Wisdom": self.wisdom,
        "Charisma": self.charisma,
        "Hitpoints": self.hitpoints
        }
        
        try:
            with open(filename, 'x') as f:
                json.dump(charDict, f, sort_keys=True, indent=4)
                print("Save successful")
        except FileExistsError:
            while True:
                print("The file '%s' already exists, do you want to overwrite it?" % filename)
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
        return "Name: %s\nRace: %s\nClass: %s\nStrength: %s\nDexterity: %s\nConstitution: %s\nIntelligence: %s\nWisdom: %s\nCharisma: %s\nHitpoints: %s\n" \
        % (str(self.name), str(self.race), str(self.role), str(self.strength), str(self.dexterity), str(self.constitution), str(self.intelligence), str(self.wisdom), str(self.charisma), str(self.hitpoints))

#----------------------------------------------------------------------------
def load_char(filename):
    """ Loads a Character from a json object. """
    try:
        with open(filename, 'r') as savefile:
            charDict = json.load(savefile)
    except FileNotFoundError:
        print("That file could not be found :(")
        return
    
    savedChar = Character(charDict["Name"], charDict["Race"], charDict["Role"])
    
    savedChar.setStrength(charDict["Strength"])
    savedChar.setDexterity(charDict["Dexterity"])
    savedChar.setConstitution(charDict["Constitution"])
    savedChar.setIntelligence(charDict["Intelligence"])
    savedChar.setWisdom(charDict["Wisdom"])
    savedChar.setCharisma(charDict["Charisma"])
    savedChar.setHitpoints(charDict["Hitpoints"])
    
    print("Character %s sucessfully loaded" % savedChar.getName())
    return savedChar

def query_save(player):
    """ Ask whether to save a Character or not. """
    while True:
        print("Do you want to save this character?")
        print("Yes to save or No to continue without saving")
        conf = input(">")
        conf = conf.upper()
        if conf == "Y" or conf == "YES":
            print("Enter a name for this save, or 'default' to use the character's name")
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
        for i in range(6):
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

#----------------------------------------------------------------------------
def race_gen():
    """ Race generation for a Character. """
    while True:
        print()
        print("What race do you want to play as?")
        print("You can choose from the following: %s" % rpgSystem["Races"])
        print('Type "random" for a random race')
        race = input(">")
        race = race.title()        # .title works for Half-Elf etc.
        
        if race.lower() == "random":
            race = random.choice(rpgSystem["Races"])
            while True:
                print("Is a %s fine?" % race)
                print("Type Yes to confirm, No to re-random, or X to pick for yourself")
                confirm = input(">")
                confirm = confirm.upper()
                if confirm == "Y" or confirm == "YES":
                    print("You are a %s!" % race)
                    return race
                elif confirm == "X":
                    race = "X"
                    break
                elif confirm == "N" or confirm == "NO":
                    race = random.choice(rpgSystem["Races"])
                else:
                    print("Invalid command")
        
        if race == "X":
            pass
        
        elif race not in rpgSystem["Races"]:
            print("Invalid selection\n")
            
        else:
            if race[0] in ['A', 'E', 'I', 'O', 'U']:
                print("You are an %s!" % race)
                return race
            else:
                print("You are a %s!" % race)
                return race

def role_gen():
    """
    Role generation for a Character.
    
    The term 'role' is instead of 'class' to be less confusing in the code.
    """
    while True:
        print()
        print("What class do you want to play as?")
        print("You can choose from the following: %s" % rpgSystem["Roles"])
        print('Type "random" for a random class')
        role = input(">")
        role = role.capitalize()
        
        if role.lower() == "random":
            role = random.choice(rpgSystem["Roles"])
            while True:
                print("Is a %s fine?" % role)
                print("Type Yes to confirm, No to re-random, or X to pick for yourself")
                confirm = input(">")
                confirm = confirm.upper()
                if confirm == "Y" or confirm == "YES":
                    print("You are a %s!" % role)
                    return role
                elif confirm == "X":
                    role = "X"
                    break
                elif confirm == "N" or confirm == "NO":
                    role = random.choice(rpgSystem["Roles"])
                else:
                    print("Invalid command")
        
        # avoids the "Invalid selection" print-out if the user decided to pick
        if role == "X":
            pass
        
        elif role not in rpgSystem["Roles"]:
            print("Invalid selection\n")
        
        else:
            if role[0] in ['A', 'E', 'I', 'O', 'U']:
                print("You are an %s!" % role)
                return role
            else:
                print("You are a %s!" % role)
                return role
                
def name_gen(race):
    """ Name generation. """
    while True:
        print()
        print("What do you want your character to be named")
        print('Input your name now, or type "random" for a random name based on your race')
        name = input(">")
        
        if name.lower() == "random":
            # Half-Elves don't have their own specific names
            if race == "Half-Elf":
                name = random.choice(rpgNames["Human_names"] + rpgNames["Elf_names"])
            
            else:
                race_names = race + "_names"
                name = random.choice(rpgNames[race_names])
        
        print("You are named: %s!" % name)
        return name

def points_mode():
    """ Manually generate ability scores using the points mode. """
    pDict = {}
    # json changes dict keys to strings even if they were originally integers
    for i in rpgStats["PointsCost"]:
        pDict[int(i)] = rpgStats["PointsCost"][i]
    points = rpgStats["TotalPoints"]
    
    print("You have %s points to spend" % points)
    print("The ability score to point cost is as follows: \n%s" % pDict)
    sList = [8, 8, 8, 8, 8, 8]
    print("Your current scorelist is: %s" % sList)
    
    while True:
        print("You have %s points left, do you want to leave your scores as they are and continue, or do you want to change your scores by using those points?" % points)
        print("Type 'Edit' to change your scores, or 'Continue' to leave them as they are and continue")
        conf = input(">")
        conf = conf.upper()
        if conf == "C" or conf == "CONTINUE":
            return sList
        elif conf == "E" or conf == "EDIT":
            print("Your current scorelist is: %s" % sList)
            print("Which score do you want to change?")
            print("Enter the number of the score to change (A number between 1 and 6), or Back to go back")
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
                        while valid == False:
                            print("Enter a number between 8 and 15, that you have enough points for, or Back to go back")
                            scoreI = input(">")
                            if scoreI.upper() == "B" or scoreI.upper() == "BACK":
                                valid = True
                            else:
                                try:
                                    scoreI = int(scoreI)
                                except ValueError:
                                    print("You must enter a number")
                                else:
                                    if scoreI < min(pDict):
                                        print("You are not allowed a score less than %s with this method" % min(pDict))
                                    elif scoreI > max(pDict):
                                        print("You are not allowed a score greater than %s with this method" % max(pDict))
                                    elif points - (pDict[scoreI] - pDict[sList[sIndex]]) < 0:
                                        print("You have insufficient points for this score")
                                    else:
                                        points -= (pDict[scoreI] - pDict[sList[sIndex]])
                                        sList[sIndex] = scoreI
                                        valid = True
        else:
            print("Invalid command")

def stat_gen():
    """ Generate ability scores using whatever mode is chosen. """
    while True:
        print()
        print("Do you want to generate your stats by die rolling, the point buy system, or take the standard scores")
        print("This step is just generating the list of scores, you will assign them to the stats you choose in the following step")
        print('Type "dice" to have them generated for you, "points" to use the point buy system, or "standard" to get the scores 15, 14, 13, 12 ,10, 8')
        stat_mode = input(">")
        stat_mode = stat_mode.lower()
        if stat_mode == "standard":
            sList = [15, 14, 13, 12, 10, 8]
            print("Your stats are %s" % sList)
            return sList
        
        elif stat_mode == "dice":
            rerolls = 2
            sList = stat_roll()
            while rerolls >= 0:
                print("Your stats are %s" % sList)
                if rerolls > 0:
                    print("Do you want to keep these or reroll? %s rerolls remaining" % rerolls)
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
                    print("You are out of rerolls, so I guess you're keeping those :P")
                    return sList
        
        elif stat_mode == "points":
            return points_mode()
        
        else:
            print("Invalid command")
            

def auto_assign(player):
    """ Assigns the character's ability scores based on its class."""
    
    player.strength = player.scorelist[rpgStats["RoleStats"][player.role]["StrengthPriority"]]
    player.dexterity = player.scorelist[rpgStats["RoleStats"][player.role]["DexterityPriority"]]
    player.constitution = player.scorelist[rpgStats["RoleStats"][player.role]["ConstitutionPriority"]]
    player.intelligence = player.scorelist[rpgStats["RoleStats"][player.role]["IntelligencePriority"]]
    player.wisdom = player.scorelist[rpgStats["RoleStats"][player.role]["WisdomPriority"]]
    player.charisma = player.scorelist[rpgStats["RoleStats"][player.role]["CharismaPriority"]]
    player.hitpoints = rpgStats["RoleStats"][player.role]["HitpointsBase"] + player.calc_mod(player.constitution)
    

def add_bonuses(player):
    """ Bases the character's bonuses on its race. """

    player.strength += rpgStats["RaceStats"][player.race]["StrengthBonus"]
    player.dexterity += rpgStats["RaceStats"][player.race]["DexterityBonus"]
    player.constitution += rpgStats["RaceStats"][player.race]["ConstitutionBonus"]
    player.intelligence += rpgStats["RaceStats"][player.race]["IntelligenceBonus"]
    player.wisdom += rpgStats["RaceStats"][player.race]["WisdomBonus"]
    player.charisma += rpgStats["RaceStats"][player.race]["CharismaBonus"]
    
    # Half-Elves get +1 to 2 scores, randomly chosen for now
    if player.race == "Half-Elf":
        
        a = random.choice([player.strength, player.dexterity, player.constitution, \
        player.intelligence, player.wisdom, player.charisma])
        a += 1
        
        b = random.choice([player.strength, player.dexterity, player.constitution, \
        player.intelligence, player.wisdom, player.charisma])
        b += 1
    

def modifier_assign(player):
    """ Assigns modifiers (just hitpoints for now actually). """
    
    player.hitpoints = rpgStats["RoleStats"][player.role]["HitpointsBase"] + player.calc_mod(player.constitution)
    

def score_assignment(player):
    """ Assignment of scores from scorelist to abilities. """
    while True:
        print()
        print("Do you want to manually assign the scores generated in the previous step to your attributes, or do you want them to be automatically assigned as best fits your class?")
        print("Type Yes for manual assignment or No for automatic assignment")
        assign_mode = input(">")
        assign_mode = assign_mode.upper()
        if assign_mode == "N" or assign_mode == "NO":
            auto_assign(player)
            break
        
        elif assign_mode == "Y" or assign_mode == "YES":
            sList = player.getScorelist()
            sListCopy = sList.copy()
            abilityCopy = rpgSystem["Attributes"].copy()
            
            while True:
                print("Your scores to assign are: %s" % sListCopy)
                i = sListCopy[0]
                print("What attribut to you want to be %s?" % i)
                print("Choose from %s" % abilityCopy)
                abil = input(">")
                abil = abil.capitalize()
                if abil not in abilityCopy:
                    print("That attribute is not available")
                
                else:
                    if abil == "Strength":
                        player.setStrength(i)
                    if abil == "Dexterity":
                        player.setDexterity(i)
                    if abil == "Constitution":
                        player.setConstitution(i)
                    if abil == "Intelligence":
                        player.setIntelligence(i)
                    if abil == "Wisdom":
                        player.setWisdom(i)
                    if abil == "Charisma":
                        player.setCharisma(i)
                    
                    abilityCopy.remove(abil)
                    sListCopy.remove(i)
                
                if sListCopy == []:
                    break
            
            add_bonuses(player)
            break

        else:
            print("Invalid input")
        
