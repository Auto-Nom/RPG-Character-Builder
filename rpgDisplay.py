# -*- coding: utf-8 -*-
"""
GUI for RPG Character Builder

@author: auto_nom
"""

import sys
import random
import json

from PyQt5.QtCore import Qt, pyqtSignal, QObject, QMimeData
from PyQt5.QtGui import QIcon, QFont, QColor, QPixmap, QDrag, QIntValidator
from PyQt5.QtWidgets import(QApplication, QMainWindow, QWidget, QAction,
                            QPushButton, QMessageBox, QDesktopWidget, QToolTip,
                            QTextEdit, QLabel, QLineEdit,
                            QHBoxLayout, QVBoxLayout, QGridLayout,
                            QInputDialog, QFileDialog, QCheckBox, QFrame,
                            QSlider, QSplitter, QComboBox, QTabWidget)

import rpgSystem as rs


class MainW(QMainWindow):
    """ Main window of the program."""

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.tab_widget = TabWidget()
        self.setCentralWidget(self.tab_widget)

        # Exit action to add to menu and toolbar
        exitAction = QAction(QIcon('Icons/Close.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        # Open file action
        openFile = QAction(QIcon('Icons/Storage.ico'), '&Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.openDialog)

        # Save file action
        saveFile = QAction(QIcon('Icons/Document.ico'), '&Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.saveDialog)

        # New tab action
        tabAction = QAction(QIcon('Icons/New.png'), 'New &Tab', self)
        tabAction.setShortcut('Ctrl+T')
        tabAction.setStatusTip('New Tab')
        tabAction.triggered.connect(self.tab_widget.newTab)

        self.statusBar()
        menubar = self.menuBar()
#        menubar.setNativeMenuBar(False)        # for MacOS, thus commented out
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(tabAction)

        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(openFile)
        self.toolbar.addAction(saveFile)
        self.toolbar.addAction(tabAction)

        self.resize(640, 480)
        self.center()

        self.statusBar().showMessage('Ready')
        self.setWindowTitle('RPG Character Builder')
        self.setWindowIcon(QIcon('Icons/paper.ico'))
        self.show()

    def center(self):
        """ Center the window on the screen."""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openDialog(self):
        """ Open and load a saved Character file."""

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            # Create a new tab to display the character in
            x = self.tab_widget.newTab()
            self.tab_widget.tabs.setCurrentWidget(x)
            try:
                self.tab_widget.tabs.currentWidget().PC = (
                                    rs.load_char(fname[0]))
            except json.decoder.JSONDecodeError:
                QMessageBox.question(self, 'Invalid filetype',
                                     "That file could not be loaded",
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.tab_widget.tabs.currentWidget().rndmBtn.hide()
                self.tab_widget.tabs.currentWidget().newBtn.hide()
                self.tab_widget.tabs.currentWidget().cdw = CharDisplayW(
                                    self.tab_widget.tabs.currentWidget())
                self.tab_widget.tabs.currentWidget().layout.addWidget(
                                self.tab_widget.tabs.currentWidget().cdw)

    def saveDialog(self):
        """ Save a Character to a file."""

        fname = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        if fname[0]:

            char = self.tab_widget.tabs.currentWidget().PC
            filename = fname[0]

            charDict = {
                        "Name": char.name,
                        "Race": char.race,
                        "Role": char.role,
                        "Attributes": char.attribDict,
                        "Hitpoints": char.hitpoints
                        }

            with open(filename, 'w') as f:
                json.dump(charDict, f, sort_keys=True, indent=4)
                print("Save successful")

    def closeEvent(self, event):
        """ Confirm the user wants to quit."""

        reply = QMessageBox.question(self, 'Goodbye',
                                     "Are you sure you want to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class TabWidget(QWidget):
    """ Widget to display tabs on."""

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)
        # self.tabList = []

        # Create actual tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        self.numTabs = 0
        self.newTab()
        self.tabs.resize(300, 200)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def newTab(self):
        """ Add and switch to a new tab."""

#        self.tabList.append(Tab())
#        self.tabs.addTab(self.tabList[self.numTabs],
#                         "Tab &" + str(self.numTabs))

        x = Tab()
        self.tabs.addTab(x, "Tab &" + str(self.numTabs))
        self.tabs.setCurrentWidget(x)

        self.numTabs += 1
        return x


class Tab(QWidget):
    """ A tab to display in the tab widget."""

    def __init__(self):
        super().__init__()

        # Each tab will have a character local to it
        self.PC = rs.Character(None, None, None)

        self.layout = QVBoxLayout(self)

        # Button to create a new character
        self.newBtn = QPushButton("New Character")
        self.newBtn.setMaximumSize(200, 30)
        self.newBtn.clicked.connect(self.newChar)
        self.layout.addWidget(self.newBtn)

        # Button to create a random character
        self.rndmBtn = QPushButton("Random Character")
        self.rndmBtn.setMaximumSize(200, 30)
        self.rndmBtn.clicked.connect(self.randomChar)
        self.layout.addWidget(self.rndmBtn)

        # Button to use the dice widget
        self.diceBtn = QPushButton("Dice Rolling")
        self.diceBtn.setMaximumSize(200, 30)
        self.diceBtn.clicked.connect(self.diceRoller)
        self.layout.addWidget(self.diceBtn)

        self.setLayout(self.layout)

    def newChar(self):
        """ Start the process of creating a new character."""
        self.rndmBtn.hide()
        self.newBtn.hide()
        self.diceBtn.hide()
        self.ncw = NewCharW(self)
        self.layout.addWidget(self.ncw)

    def randomChar(self):
        """ Randomly generate a character."""

        race = random.choice(rs.rpgData["Races"])
        role = random.choice(rs.rpgData["Roles"])

        # Half-Elves do not have unique names
        # Need to make this non-hardcoded; put in the data files somehow
        # Easiest would be copy paste elf+human names into Half-Elf_names
        if race == "Half-Elf":
            name = random.choice(rs.namesData["Human_names"] +
                                 rs.namesData["Elf_names"])
        else:
            race_names = race + "_names"
            try:
                name = random.choice(rs.namesData[race_names])
            except KeyError:
                name = random.choice(rs.namesData["Common_Names"])

        Char = rs.Character(name, race, role)
        sList = rs.stat_roll()
        Char.setScorelist(sList)
        rs.auto_assign(Char)
        rs.add_bonuses(Char)
        rs.modifier_assign(Char)

        self.PC = Char

        # Don't hide random button here, for convenience to re-random
        self.newBtn.hide()
        self.diceBtn.hide()
        try:
            self.layout.removeWidget(self.cdw)
            self.cdw.close()
            self.layout.update()
        except AttributeError:
            pass

        self.cdw = CharDisplayW(self)
        self.layout.addWidget(self.cdw)

    def diceRoller(self):

        self.rndmBtn.hide()
        self.newBtn.hide()
        self.diceBtn.hide()
        self.drw = DiceRollW(self)
        self.layout.addWidget(self.drw)


class NewCharW(QWidget):
    """ Choose the name, race, and role of a new character."""

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.initUI()

    def initUI(self):

        # Layout
        grid = QGridLayout()
        grid.setSpacing(10)

        # Name Selection
        self.nameLabel = QLabel('What do you want to be named?')
        self.hello = QLabel('Hello')
        self.nameEdit = QLineEdit()
        self.nameEdit.setFixedWidth(100)
        self.nameEdit.textChanged[str].connect(self.onChanged)
        self.nameRand = QPushButton("Random")
        self.nameRand.clicked.connect(self.randomName)

        grid.addWidget(self.nameLabel, 0, 0)
        grid.addWidget(self.nameEdit, 0, 1)
        grid.addWidget(self.nameRand, 0, 2)
        grid.addWidget(self.hello, 0, 3)

        # Race Selection
        self.racePrompt = QLabel("Choose your race:")
        self.raceLabel = QLabel("Race")
        self.raceSel = QComboBox(self)

        for i in rs.Races:
            self.raceSel.addItem(i)

        self.raceSel.currentIndexChanged[str].connect(self.SelActivated)
        self.raceRand = QPushButton("Random")
        self.raceRand.clicked.connect(self.randomRace)

        grid.addWidget(self.racePrompt, 1, 0)
        grid.addWidget(self.raceSel, 1, 1)
        grid.addWidget(self.raceRand, 1, 2)
        grid.addWidget(self.raceLabel, 1, 3)

        # Role Selection
        self.rolePrompt = QLabel("Choose your class:")
        self.roleLabel = QLabel("Class")
        self.roleSel = QComboBox(self)

        for i in rs.Roles:
            self.roleSel.addItem(i)

        self.roleSel.currentIndexChanged[str].connect(self.SelActivated)
        self.roleRand = QPushButton("Random")
        self.roleRand.clicked.connect(self.randomRole)

        grid.addWidget(self.rolePrompt, 2, 0)
        grid.addWidget(self.roleSel, 2, 1)
        grid.addWidget(self.roleRand, 2, 2)
        grid.addWidget(self.roleLabel, 2, 3)

        # Submit button
        self.submitBtn = QPushButton("Next")
        self.submitBtn.clicked.connect(self.submitChar)
        grid.addWidget(self.submitBtn, 3, 4)

        self.setLayout(grid)

        self.name = self.nameEdit.text()
        self.race = self.raceSel.currentText()
        self.role = self.roleSel.currentText()

    def SelActivated(self, text):
        """ Update to the chosen race or role when selected."""

        sender = self.sender()

        if sender == self.raceSel:
            self.raceLabel.setText("Race Description")
            self.raceLabel.adjustSize()
            self.race = text

        elif sender == self.roleSel:
            self.roleLabel.setText("Class Description")
            self.roleLabel.adjustSize()
            self.role = text

    def onChanged(self, text):
        """ Update the name."""

        self.hello.setText('Hello, ' + text)
        self.hello.adjustSize()
        self.name = text

    def randomName(self):
        """ Generate a random name based on the chosen race."""

        if self.race == "Half-Elf":
            self.name = random.choice(rs.namesData["Human_names"] +
                                      rs.namesData["Elf_names"])
        else:
            race_names = self.race + "_names"
            try:
                self.name = random.choice(rs.namesData[race_names])
            except KeyError:
                self.name = random.choice(rs.namesData["Common_Names"])

        self.nameEdit.setText(self.name)

    def randomRace(self):
        """ Choose a random race."""

        self.race = random.choice(rs.rpgData["Races"])
        self.raceSel.setCurrentText(self.race)

    def randomRole(self):
        """ Choose a random role."""

        self.role = random.choice(rs.rpgData["Roles"])
        self.roleSel.setCurrentText(self.role)

    def submitChar(self):
        """ Create the actual Character object and move to the next step."""

        self.hide()

        self.parent.PC = rs.Character(self.name, self.race, self.role)

        # Create the widget for the next step of character generation
        self.parent.sew = StatEditW(self.parent)
        self.parent.layout.addWidget(self.parent.sew)
        self.parent.sew.show()
        self.close()


class StatEditW(QWidget):
    """ A widget for generating ability scores."""

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.sList = []

        self.initUI()

    def initUI(self):

        # Layout
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # Label describing the step
        self.sLabel = QLabel('How do you want to generate your scores')
        self.grid.addWidget(self.sLabel, 0, 0, 1, 5)

        # Button for using the dice method
        self.diceBtn = QPushButton("Dice")
        self.diceBtn.clicked.connect(self.btnClicked)
        self.grid.addWidget(self.diceBtn, 1, 0)

        # Button for using the points method
        self.pointsBtn = QPushButton("Points")
        self.pointsBtn.clicked.connect(self.btnClicked)
        self.grid.addWidget(self.pointsBtn, 1, 1)

        # Button for taking the standard scores
        self.stdBtn = QPushButton("Standard")
        self.stdBtn.clicked.connect(self.btnClicked)
        self.grid.addWidget(self.stdBtn, 1, 2)

        # Button to go to the next step
        self.nxtBtn = QPushButton("Next")
        self.nxtBtn.clicked.connect(self.setList)
        self.grid.addWidget(self.nxtBtn, 3, 3)
        self.nxtBtn.hide()

        # Button to go back to the previous step
        self.bkBtn = QPushButton("Back")
        self.bkBtn.clicked.connect(self.goBack)
        self.grid.addWidget(self.bkBtn, 3, 0)

        # Label for the scores generated
        self.scores = QLabel(" ")
        self.scores.setFont(QFont("Serif", 16))
        self.grid.addWidget(self.scores, 2, 1, 1, 5)

        self.setLayout(self.grid)
        self.show()

    def btnClicked(self):
        """ Generate points using the method of the button that was clicked."""

        sender = self.sender()

        # Dice method
        if sender == self.diceBtn:
            self.diceBtn.hide()
            self.pointsBtn.hide()
            self.stdBtn.hide()
            self.sLabel.hide()
            self.nxtBtn.show()

            self.sList = rs.stat_roll()

            # At the moment a badly designed way to show the scores
            self.scoreL = '| '
            for i in self.sList:
                self.scoreL += str(i) + ' | '

            self.scores.setText(self.scoreL)

        # Points method
        elif sender == self.pointsBtn:
            self.diceBtn.hide()
            self.pointsBtn.hide()
            self.stdBtn.hide()
            self.sLabel.hide()

            # Use the points widget class
            pointW = pointsW(self)
            self.grid.addWidget(pointW, 2, 1, 1, 3)

        # Standard scores method
        elif sender == self.stdBtn:
            self.diceBtn.hide()
            self.pointsBtn.hide()
            self.stdBtn.hide()
            self.nxtBtn.show()
            self.sLabel.hide()

            self.sList = rs.statsData["StandardPoints"]

            # At the moment a badly designed way to show the scores
            self.scoreL = '| '
            for i in self.sList:
                self.scoreL += str(i) + ' | '
            self.scores.setText(self.scoreL)

    def goBack(self):
        """ Go back to the previous step."""
        self.hide()
        self.parent.ncw = NewCharW(self.parent)
        self.parent.layout.addWidget(self.parent.ncw)
        self.parent.ncw.show()
        self.close()

    def setList(self):
        """ Set the character's scorelist and move to the next step"""
        self.hide()
        self.sList.sort(reverse=True)
        self.parent.PC.setScorelist(self.sList)

        self.parent.saw = StatAssignW(self.parent)
        self.parent.layout.addWidget(self.parent.saw)
        self.parent.saw.show()
        self.close()


class valChangeW(QWidget):
    """ Widget for increasing or decreasing a score."""

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.val = min(parent.pDict)

        self.initUI()

    def initUI(self):

        # Button to increase a score
        self.upBtn = QPushButton("^")
        self.upBtn.setMaximumSize(30, 30)
        self.upBtn.clicked.connect(self.changeVal)
        self.layout.addWidget(self.upBtn)

        # Label to display the score
        self.lbl = QLabel(str(self.val))
        self.lbl.setMaximumSize(30, 30)
        self.layout.addWidget(self.lbl)

        # Button to decrease a score
        self.dwnBtn = QPushButton("V")
        self.dwnBtn.setMaximumSize(30, 30)
        self.dwnBtn.clicked.connect(self.changeVal)
        self.layout.addWidget(self.dwnBtn)

        self.setLayout(self.layout)

    def changeVal(self):
        """ Change the value if possible, and update total points."""
        sender = self.sender()

        if sender == self.upBtn:
            newval = self.val + 1

            # Ensure the score is valid
            if newval > max(self.parent.pDict):
                MW.statusBar().showMessage('You may not have a higher score')

            elif (self.parent.points - (self.parent.pDict[newval] -
                                        self.parent.pDict[self.val])) < 0:
                MW.statusBar().showMessage('INSUFFICIENT POINTS')
            else:
                # Update the total points
                self.parent.points -= (self.parent.pDict[newval] -
                                       self.parent.pDict[self.val])
                self.parent.pointsLbl.setText("Points: " +
                                              str(self.parent.points))
                self.val = newval
                self.lbl.setText(str(self.val))
                MW.statusBar().showMessage(' ')

        elif sender == self.dwnBtn:
            newval = self. val - 1

            # When decreasing the only issue would be a below minimum score
            if newval < min(self.parent.pDict):
                MW.statusBar().showMessage('You may not have a lower score')
            else:
                self.parent.points -= (self.parent.pDict[newval] -
                                       self.parent.pDict[self.val])
                self.parent.pointsLbl.setText("Points: " +
                                              str(self.parent.points))
                self.val = newval
                self.lbl.setText(str(self.val))
                MW.statusBar().showMessage(' ')


class pointsW(QWidget):
    """ Widget for using the points method of score generation."""

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.layout = QHBoxLayout(self)

        # Create the dictionary mapping scores to their point cost
        self.pDict = {}
        for i in rs.statsData["PointsCost"]:
            self.pDict[int(i)] = rs.statsData["PointsCost"][i]
        self.points = rs.statsData["PointsTotal"]
        self.sDict = {}
        self.initUI()

    def initUI(self):

        # Label showing total points
        self.pointsLbl = QLabel("Points: " + str(self.points))
        self.layout.addWidget(self.pointsLbl)

        # Create the necessary amount of valChange widgets
        for i in range(len(rs.Attributes)):
            self.sDict[i] = valChangeW(self)
            self.layout.addWidget(self.sDict[i])

        # Button for setting the points
        self.doneBtn = QPushButton("Done")
        self.doneBtn.clicked.connect(self.fDone)
        self.layout.addWidget(self.doneBtn)

        self.setLayout(self.layout)

    def fDone(self):
        """ Set the scores into the parent widget."""
        for i in self.sDict.values():
            self.parent.sList.append(i.val)
        self.hide()
        self.parent.scoreL = '| '
        for i in self.parent.sList:
            self.parent.scoreL += str(i) + ' | '
        self.parent.scores.setText(self.parent.scoreL)
        self.parent.nxtBtn.show()


class AttributeBox(QWidget):
    """ A widget for assigning a score to an attribute."""

    def __init__(self, text, parent):
        super().__init__(parent)

        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.text = text

        self.initUI(self.text)

    def initUI(self, text):

        # Validator to ensure only a positive int less then 1000 is entered
        validator = QIntValidator(0, 999)

        # Label for the attribute name
        self.aLabel = QLabel(str(text) + ": ")
        self.layout.addWidget(self.aLabel)

        # Box to enter the desired score into
        self.aEdit = QLineEdit()
        self.aEdit.setMaximumWidth(30)
        self.aEdit.setValidator(validator)
        self.layout.addWidget(self.aEdit)

        # Button to set the score
        self.aSet = QPushButton("Set")
        self.aSet.setCheckable(True)
        self.aSet.clicked[bool].connect(self.setAttrib)
        self.layout.addWidget(self.aSet)

        self.setLayout(self.layout)

    def setAttrib(self, pressed):
        """ Set an attribute's score."""
        try:
            val = int(self.aEdit.text())
        except ValueError:
            # Even though there's a validator, a blank box causes a ValueError
            MW.statusBar().showMessage(' ')
            self.aSet.setChecked(False)
        else:
            if pressed:
                # Set the value if it is valid, and update the list of values
                if val in self.parent.sList:
                    self.parent.sList.remove(val)
                    self.parent.aDict[self.text] = val
                    self.aEdit.setReadOnly(True)
                    MW.statusBar().showMessage(' ')
                    self.parent.listS.setText(str(self.parent.sList))
                else:
                    self.aSet.setChecked(False)
                    MW.statusBar().showMessage('THAT VALUE IS NOT AVAILABLE')

            # Unset the value, and update the list
            else:
                self.parent.sList.append(val)
                self.parent.aDict[self.text] = 0
                self.aEdit.setReadOnly(False)
                self.parent.listS.setText(str(self.parent.sList))
                MW.statusBar().showMessage(' ')


class StatAssignW(QWidget):
    """ A widget to assign scores to attributes."""

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.aDict = {}
        self.sDict = {}

        self.initUI()

    def initUI(self):

        self.sList = self.parent.PC.getScorelist()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # Prompt on what to do
        self.assignPrompt = QLabel("Assign your scores to attributes")
        self.grid.addWidget(self.assignPrompt, 0, 0)

        # Button to advance to the next stage
        self.nxtBtn = QPushButton("Next")
        self.nxtBtn.clicked.connect(self.setAttribs)
        self.grid.addWidget(self.nxtBtn, 1, 5)

        # Button to automatically assign scores
        self.autoBtn = QPushButton("Auto-Assign")
        self.autoBtn.clicked.connect(self.autoAttribs)
        self.grid.addWidget(self.autoBtn, 0, 4)

        # Button to go back to the previous step
        self.bkBtn = QPushButton("Back")
        self.bkBtn.clicked.connect(self.goBack)
        self.grid.addWidget(self.bkBtn, 1, 0)

        # List of available scores
        self.listS = QLabel(str(self.sList))
        self.listS.setFont(QFont("Serif", 12))
        self.grid.addWidget(self.listS, 2, 0)

        # Add the required widgets for assigning scores
        for i in range(len(rs.Attributes)):
            self.sDict[i] = (AttributeBox(str(rs.Attributes[i]), self))
            self.grid.addWidget(self.sDict[i], i+1, 4)

        self.setLayout(self.grid)
        self.show()

    def goBack(self):
        """ Go back to the previous step."""
        self.hide()
        self.parent.sew = StatEditW(self.parent)
        self.parent.layout.addWidget(self.parent.sew)
        self.parent.sew.show()
        self.close()

    def setAttribs(self):
        """ Set the character's attributes as specified, then display it."""

        # Ensure all attributes have been set
        for i in self.sDict:
            if self.sDict[i].aSet.isChecked() is False:
                MW.statusBar().showMessage('SET ALL ATTRIBUTES FIRST')
                return

        self.hide()

        # Set the attributes and perform the rest of the character generation
        for i in self.aDict:
            self.parent.PC.setAttrib(i, int(self.aDict[i]))
        rs.add_bonuses(self.parent.PC)
        rs.modifier_assign(self.parent.PC)

        # Display the finished character
        self.parent.cdw = CharDisplayW(self.parent)
        self.parent.layout.addWidget(self.parent.cdw)
        self.parent.cdw.show()
        self.close()

    def autoAttribs(self):
        """ Automatically assign scores to attributes, then display."""

        self.hide()
        rs.auto_assign(self.parent.PC)
        rs.add_bonuses(self.parent.PC)
        rs.modifier_assign(self.parent.PC)

        self.parent.cdw = CharDisplayW(self.parent)
        self.parent.layout.addWidget(self.parent.cdw)
        self.parent.cdw.show()
        self.close()


class CharDisplayW(QWidget):
    """ A widget to display a character."""

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.aDict = {}

        self.initUI()

    def initUI(self):

        # The character to display
        self.char = self.parent.PC
        self.attribs = self.char.getAttribDict()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # Name label
        self.cName = QLabel(self.char.getName())
        self.grid.addWidget(self.cName, 0, 0)

        # Race label
        self.cRace = QLabel(self.char.getRace())
        self.grid.addWidget(self.cRace, 1, 0)

        # Role label
        self.cRole = QLabel(self.char.getRole())
        self.grid.addWidget(self.cRole, 2, 0)

        # Space
        self.grid.setColumnMinimumWidth(1, 100)

        i = 0
        # Labels for all the attributes
        for k, v in self.attribs.items():
            self.aDict[k] = QLabel(str(k) + ": " + str(v))
            self.grid.addWidget(self.aDict[k], i, 2)
            i += 1

        # Label for hitpoints
        self.cHP = QLabel("Hitpoints: " + str(self.char.getHitpoints()))
        self.grid.addWidget(self.cHP, i+1, 2)

        # Button for editing the character
        self.editBtn = QPushButton("Edit")
        self.editBtn.setMaximumSize(100, 30)
        self.editBtn.clicked.connect(self.editChar)
        self.grid.addWidget(self.editBtn, 5, 0)

        self.setLayout(self.grid)
        self.show()

    def editChar(self):
        """ Edit a character's stats."""

        # if the character was randomed
        if self.parent.rndmBtn.isVisible():
            self.wasRandom = True
        else:
            self.wasRandom = False

        self.parent.rndmBtn.hide()
        self.hide()
        self.parent.cew = CharEditW(self.parent)
        self.parent.layout.addWidget(self.parent.cew)
        self.parent.cew.show()
        self.close()


class AttributeEdit(QWidget):
    """ A widget to edit a character's attribute score."""

    def __init__(self, text, parent):
        super().__init__(parent)

        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.text = text

        self.initUI(self.text)

    def initUI(self, text):

        # Validator to ensure an int < 1000 is entered
        validator = QIntValidator(0, 999)

        # Label for the attribute
        self.aLabel = QLabel(str(text) + ": ")
        self.layout.addWidget(self.aLabel)

        # Box to insert the new score
        self.aEdit = QLineEdit()
        self.aEdit.setText(str(self.parent.attribs[text]))
        self.aEdit.setMaximumWidth(30)
        self.aEdit.setValidator(validator)
        self.layout.addWidget(self.aEdit)

        self.setLayout(self.layout)

    def setVal(self):
        """ Set the attribute score."""
        try:
            self.val = int(self.aEdit.text())
        except ValueError:
            # If no value is entered, set to zero
            self.val = 0
        finally:
            self.parent.aDict[self.text] = self.val


class CharEditW(QWidget):
    """ A widget for editing a character."""

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.aDict = {}
        self.sDict = {}

        self.initUI()

    def initUI(self):

        # The character to edit
        self.char = self.parent.PC
        self.attribs = self.char.getAttribDict()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # Label to display the name
        self.cName = QLabel(self.char.getName())
        self.grid.addWidget(self.cName, 0, 0)

        # Label to display the race
        self.cRace = QLabel(self.char.getRace())
        self.grid.addWidget(self.cRace, 1, 0)

        # Label to display the role
        self.cRole = QLabel(self.char.getRole())
        self.grid.addWidget(self.cRole, 2, 0)

        self.grid.setColumnMinimumWidth(1, 100)

        # Add the widgets for editing attributes
        for i in range(len(rs.Attributes)):
            self.sDict[i] = (AttributeEdit(str(rs.Attributes[i]), self))
            self.grid.addWidget(self.sDict[i], i+1, 2)

        # Button to go back to the display screen
        self.backBtn = QPushButton("Go Back")
        self.backBtn.clicked.connect(self.goBack)
        self.grid.addWidget(self.backBtn, 5, 0)

        # Button to set the edits and then display the character
        self.confBtn = QPushButton("Confirm")
        self.confBtn.clicked.connect(self.confirmEdit)
        self.grid.addWidget(self.confBtn, 6, 0)

        self.setLayout(self.grid)
        self.show()

    def goBack(self):
        """ Go back to the display screen without setting the edits."""
        self.hide()
        # if character was randomed and hasn't been edited, show random button
        if self.parent.cdw.wasRandom:
            self.parent.rndmBtn.show()

        self.parent.cdw = CharDisplayW(self.parent)
        self.parent.layout.addWidget(self.parent.cdw)
        self.parent.cdw.show()
        self.close()

    def confirmEdit(self):
        """ Set the edits and update the character, then display it."""

        self.hide()
        for i in self.sDict:
            self.sDict[i].setVal()

        for i in self.aDict:
            self.parent.PC.setAttrib(i, int(self.aDict[i]))

        rs.modifier_assign(self.parent.PC)
        self.parent.cdw = CharDisplayW(self.parent)
        self.parent.layout.addWidget(self.parent.cdw)
        self.parent.cdw.show()
        self.close()


class DiceRollW(QWidget):
    """ A widget for rolling dice."""
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.initUI()

    def initUI(self):

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.topLbl = QLabel("<i>Dovie'andi se tovya sagain</i> - Mat Cauthon")
        self.topLbl.setToolTip("It's time to roll the dice")
        self.grid.addWidget(self.topLbl, 0, 0)

        self.resultLbl = QLabel(" ")
        self.grid.addWidget(self.resultLbl, 1, 0)

        # 20 sided dice
        self.d20 = QPushButton("D20")
        self.d20.clicked.connect(self.d20Roll)
        self.grid.addWidget(self.d20, 2, 1)

        # 4 sided dice
        self.d4 = QPushButton("D4")
        self.d4.clicked.connect(self.diceRoll)
        self.grid.addWidget(self.d4, 3, 1)

        # 6 sided dice
        self.d6 = QPushButton("D6")
        self.d6.clicked.connect(self.diceRoll)
        self.grid.addWidget(self.d6, 4, 1)

        # 8 sided dice
        self.d8 = QPushButton("D8")
        self.d8.clicked.connect(self.diceRoll)
        self.grid.addWidget(self.d8, 5, 1)

        # 10 sided dice
        self.d10 = QPushButton("D10")
        self.d10.clicked.connect(self.diceRoll)
        self.grid.addWidget(self.d10, 6, 1)

        # 12 sided dice
        self.d12 = QPushButton("D12")
        self.d12.clicked.connect(self.diceRoll)
        self.grid.addWidget(self.d12, 7, 1)

        # 100 sided dice
        self.d100 = QPushButton("D100")
        self.d100.clicked.connect(self.diceRoll)
        self.grid.addWidget(self.d100, 8, 1)

        self.setLayout(self.grid)

    def d20Roll(self):
        roll = random.randint(1, 20)
        if roll == 20:
            self.topLbl.setText("CRITICAL SUCCESS!")
        elif roll == 1:
            self.topLbl.setText("CRITICAL FAILURE!")
        else:
            self.topLbl.setText("You rolled: ")

        self.resultLbl.setText(str(roll))

    def diceRoll(self, sender):
        sender = self.sender()
        label = int(sender.text()[1:])

        roll = random.randint(1, label)
        self.topLbl.setText("You rolled: ")
        self.resultLbl.setText(str(roll))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MW = MainW()
    sys.exit(app.exec_())
