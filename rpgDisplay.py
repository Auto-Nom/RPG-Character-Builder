# -*- coding: utf-8 -*-
"""
GUI for RPG Character Builder

@author: auto_nom
"""

import sys
import random

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

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.tab_widget = TabWidget()
        self.setCentralWidget(self.tab_widget)

        # Exit action to add to menu and toolbar
        exitAction = QAction(QIcon('Icons/X.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        # Open file action
        openFile = QAction(QIcon('Icons/Storage.ico'), '&Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.fileDialog)

        # New tab action
        tabAction = QAction(QIcon('Icons/folder_doc.ico'), 'New &Tab', self)
        tabAction.setShortcut('Ctrl+T')
        tabAction.setStatusTip('New Tab')
        tabAction.triggered.connect(self.tab_widget.newTab)

        self.statusBar()
        menubar = self.menuBar()
#        menubar.setNativeMenuBar(False)        # for MacOS, thus commented out
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openFile)
        fileMenu.addAction(tabAction)

        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(openFile)
        self.toolbar.addAction(tabAction)

        self.resize(640, 480)
        self.center()

        self.statusBar().showMessage('Ready')
        self.setWindowTitle('RPG Character Builder')
        self.setWindowIcon(QIcon('Icons/paper.ico'))
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fileDialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:

            with open(fname[0], 'r') as f:
                data = f.read()
                self.cont.textEdit.setText(data)

    # Confirm quit
    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Goodbye',
                                     "Are you sure you want to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class TabWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.tabList = []

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.numTabs = 0
        self.newTab()
        self.tabs.resize(300, 200)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def newTab(self):

        self.tabList.append(Tab())
        self.tabs.addTab(self.tabList[self.numTabs],
                         "Tab &" + str(self.numTabs))
        self.numTabs += 1


class Tab(QWidget):

    def __init__(self):
        super().__init__()

        self.PC = rs.Character(None, None, None)

        self.layout = QVBoxLayout(self)

        self.newBtn = QPushButton("New Character")
        self.newBtn.clicked.connect(self.newChar)
        self.layout.addWidget(self.newBtn)

        self.rndmBtn = QPushButton("Random Character")
        self.rndmBtn.clicked.connect(self.randomChar)
        self.layout.addWidget(self.rndmBtn)

        self.setLayout(self.layout)

    def newChar(self):
        # New Character
        self.rndmBtn.hide()
        self.newBtn.hide()
        self.ncw = NewCharW(self)
        self.layout.addWidget(self.ncw)

    def randomChar(self):

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

        self.rndmBtn.hide()
        self.newBtn.hide()
        self.cdw = CharDisplayW(self)
        self.layout.addWidget(self.cdw)


class NewCharW(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        print(self.parent)

        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        # Name Selection
        self.nameLabel = QLabel('What do you want to be named?')
        self.hello = QLabel('Hello')
        self.nameEdit = QLineEdit()
        self.nameEdit.setFixedWidth(100)
        self.nameEdit.textChanged[str].connect(self.onChanged)
        self.nameRand = QPushButton("Random")
        self.nameRand.clicked.connect(self.randomName)

        # Race Selection
        self.racePrompt = QLabel("Choose your race:")
        self.raceLabel = QLabel("Race")
        self.raceSel = QComboBox(self)

        for i in rs.Races:
            self.raceSel.addItem(i)

        self.raceSel.currentIndexChanged[str].connect(self.SelActivated)
        self.raceRand = QPushButton("Random")
        self.raceRand.clicked.connect(self.randomRace)

        # Role Selection
        self.rolePrompt = QLabel("Choose your class:")
        self.roleLabel = QLabel("Class")
        self.roleSel = QComboBox(self)

        for i in rs.Roles:
            self.roleSel.addItem(i)

        self.roleSel.currentIndexChanged[str].connect(self.SelActivated)
        self.roleRand = QPushButton("Random")
        self.roleRand.clicked.connect(self.randomRole)

        # Submit button
        self.submitBtn = QPushButton("Next")
        self.submitBtn.clicked.connect(self.submitChar)

        # Layout
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.nameLabel, 0, 0)
        grid.addWidget(self.nameEdit, 0, 1)
        grid.addWidget(self.nameRand, 0, 2)
        grid.addWidget(self.hello, 0, 3)

        grid.addWidget(self.racePrompt, 1, 0)
        grid.addWidget(self.raceSel, 1, 1)
        grid.addWidget(self.raceRand, 1, 2)
        grid.addWidget(self.raceLabel, 1, 3)

        grid.addWidget(self.rolePrompt, 2, 0)
        grid.addWidget(self.roleSel, 2, 1)
        grid.addWidget(self.roleRand, 2, 2)
        grid.addWidget(self.roleLabel, 2, 3)

        grid.addWidget(self.submitBtn, 3, 4)

        self.setLayout(grid)

        self.name = self.nameEdit.text()
        self.race = self.raceSel.currentText()
        self.role = self.roleSel.currentText()

    def SelActivated(self, text):

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

        self.hello.setText('Hello, ' + text)
        self.hello.adjustSize()
        self.name = text

    def submitChar(self):

        self.hide()

        self.parent.PC = rs.Character(self.name, self.race, self.role)
        print(self.parent.PC.getName(), self.parent.PC.getRace(),
              self.parent.PC.getRole())
        self.parent.sew = StatEditW(self.parent)
        self.parent.layout.addWidget(self.parent.sew)
        self.parent.sew.show()
        self.close()

    def randomName(self):

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

        self.race = random.choice(rs.rpgData["Races"])
        self.raceSel.setCurrentText(self.race)

    def randomRole(self):

        self.role = random.choice(rs.rpgData["Roles"])
        self.roleSel.setCurrentText(self.role)


class StatEditW(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.sList = []

        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.sLabel = QLabel('How do you want to generate your scores')

        self.diceBtn = QPushButton("Dice")
        self.diceBtn.clicked.connect(self.btnClicked)

        self.pointsBtn = QPushButton("Points")
        self.pointsBtn.clicked.connect(self.btnClicked)

        self.stdBtn = QPushButton("Standard")
        self.stdBtn.clicked.connect(self.btnClicked)

        self.nxtBtn = QPushButton("Next")
        self.nxtBtn.clicked.connect(self.setList)

        self.bkBtn = QPushButton("Back")
        self.bkBtn.clicked.connect(self.goBack)

        self.scores = QLabel(" ")

        # Layout
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.sLabel, 0, 0)
        self.grid.addWidget(self.diceBtn, 1, 1)
        self.grid.addWidget(self.pointsBtn, 1, 2)
        self.grid.addWidget(self.stdBtn, 1, 3)
        self.grid.addWidget(self.scores, 2, 1, 1, 3)
        self.grid.addWidget(self.bkBtn, 3, 0)
        self.grid.addWidget(self.nxtBtn, 3, 1)
        self.nxtBtn.hide()

        self.setLayout(self.grid)
        self.show()

    def btnClicked(self):

        sender = self.sender()

        if sender == self.diceBtn:

            self.diceBtn.hide()
            self.pointsBtn.hide()
            self.stdBtn.hide()
            self.sLabel.hide()
            self.nxtBtn.show()

            self.sList = rs.stat_roll()

            self.scoreL = '| '

            for i in self.sList:
                self.scoreL += str(i) + ' | '

            self.scores.setText(self.scoreL)

        elif sender == self.pointsBtn:

            self.diceBtn.hide()
            self.pointsBtn.hide()
            self.stdBtn.hide()
            self.sLabel.hide()

            pointW = pointsW(self)
            self.grid.addWidget(pointW, 2, 1, 1, 3)

        elif sender == self.stdBtn:

            self.diceBtn.hide()
            self.pointsBtn.hide()
            self.stdBtn.hide()
            self.nxtBtn.show()
            self.sLabel.hide()

            self.sList = rs.statsData["StandardPoints"]
            self.scoreL = '| '
            for i in self.sList:
                self.scoreL += str(i) + ' | '
            self.scores.setText(self.scoreL)

    def goBack(self):
        self.hide()
        self.parent.ncw = NewCharW(self.parent)
        self.parent.layout.addWidget(self.parent.ncw)
        self.parent.ncw.show()
        self.close()

    def setList(self):
        self.hide()
        self.sList.sort(reverse=True)
        print(str(self.sList))
        self.parent.PC.setScorelist(self.sList)
        self.parent.saw = StatAssignW(self.parent)
        self.parent.layout.addWidget(self.parent.saw)
        self.parent.saw.show()
        self.close()


class valChangeW(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.val = min(parent.pDict)

        self.initUI()

    def initUI(self):

        self.upBtn = QPushButton("^")
        self.upBtn.setMaximumSize(25, 25)
        self.upBtn.clicked.connect(self.changeVal)
        self.lbl = QLabel(str(self.val))
        self.lbl.setMaximumSize(25, 25)
        self.dwnBtn = QPushButton("V")
        self.dwnBtn.setMaximumSize(25, 25)
        self.dwnBtn.clicked.connect(self.changeVal)

        self.layout.addWidget(self.upBtn)
        self.layout.addWidget(self.lbl)
        self.layout.addWidget(self.dwnBtn)

        self.setLayout(self.layout)

    def changeVal(self):
        sender = self.sender()

        if sender == self.upBtn:
            newval = self.val + 1

            if newval > max(self.parent.pDict):
                MW.statusBar().showMessage('You may not have a higher score')

            elif (self.parent.points - (self.parent.pDict[newval] -
                                        self.parent.pDict[self.val])) < 0:
                MW.statusBar().showMessage('INSUFFICIENT POINTS')
            else:
                self.parent.points -= (self.parent.pDict[newval] -
                                       self.parent.pDict[self.val])
                self.parent.pointsLbl.setText("Points: " +
                                              str(self.parent.points))
                self.val = newval
                self.lbl.setText(str(self.val))
                MW.statusBar().showMessage(' ')

        elif sender == self.dwnBtn:
            newval = self. val - 1

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

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.layout = QHBoxLayout(self)

        self.pDict = {}
        for i in rs.statsData["PointsCost"]:
            self.pDict[int(i)] = rs.statsData["PointsCost"][i]
        self.points = rs.statsData["PointsTotal"]
        self.sDict = {}
        self.initUI()

    def initUI(self):

        self.pointsLbl = QLabel("Points: " + str(self.points))

        self.layout.addWidget(self.pointsLbl)
        for i in range(len(rs.Attributes)):
            self.sDict[i] = valChangeW(self)
            self.layout.addWidget(self.sDict[i])

        self.dButton = QPushButton("Done")
        self.dButton.clicked.connect(self.fDone)
        self.layout.addWidget(self.dButton)

        self.setLayout(self.layout)

    def fDone(self):
        for i in self.sDict.values():
            self.parent.sList.append(i.val)
        self.hide()
        self.parent.scoreL = '| '
        for i in self.parent.sList:
            self.parent.scoreL += str(i) + ' | '
        self.parent.scores.setText(self.parent.scoreL)
        self.parent.nxtBtn.show()


class AttributeBox(QWidget):

    def __init__(self, text, parent):
        super().__init__(parent)

        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.text = text

        self.initUI(self.text)

    def initUI(self, text):

        validator = QIntValidator(0, 999)
        self.aLabel = QLabel(str(text) + ": ")
        self.aEdit = QLineEdit()
        self.aEdit.setMaximumWidth(30)
        self.aEdit.setValidator(validator)
        self.aSet = QPushButton("Set")
        self.aSet.setCheckable(True)
        self.aSet.clicked[bool].connect(self.setAttrib)

        self.layout.addWidget(self.aLabel)
        self.layout.addWidget(self.aEdit)
        self.layout.addWidget(self.aSet)

    def setAttrib(self, pressed):
        try:
            val = int(self.aEdit.text())
        except ValueError:
            MW.statusBar().showMessage(' ')
            self.aSet.setChecked(False)
        else:
            if pressed:
                if val in self.parent.sList:
                    self.parent.sList.remove(val)
                    self.parent.aDict[self.text] = val
                    self.aEdit.setReadOnly(True)
                    MW.statusBar().showMessage(' ')
                    self.parent.listS.setText(str(self.parent.sList))
                else:
                    self.aSet.setChecked(False)
                    MW.statusBar().showMessage('THAT VALUE IS NOT AVAILABLE')

            else:
                self.parent.sList.append(val)
                self.parent.aDict[self.text] = 0
                self.aEdit.setReadOnly(False)
                self.parent.listS.setText(str(self.parent.sList))
                MW.statusBar().showMessage(' ')


class StatAssignW(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.aDict = {}
        self.sDict = {}

        self.initUI()

    def initUI(self):

        self.sList = self.parent.PC.getScorelist()

        self.assignPrompt = QLabel("Assign your scores to attributes")
        self.nxtBtn = QPushButton("Next")
        self.nxtBtn.clicked.connect(self.setAttribs)

        self.autoBtn = QPushButton("Auto-Assign")
        self.autoBtn.clicked.connect(self.autoAttribs)

        self.bkBtn = QPushButton("Back")
        self.bkBtn.clicked.connect(self.goBack)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.assignPrompt, 0, 0)
        self.grid.addWidget(self.autoBtn, 0, 4)
        self.grid.addWidget(self.nxtBtn, 0, 5)
        self.grid.addWidget(self.bkBtn, 3, 0)

        self.listS = QLabel(str(self.sList))
        self.grid.addWidget(self.listS, 1, 0)

        for i in range(len(rs.Attributes)):
            self.sDict[i] = (AttributeBox(str(rs.Attributes[i]), self))
            self.grid.addWidget(self.sDict[i], i+1, 4)

        self.setLayout(self.grid)
        self.show()

    def goBack(self):
        self.hide()
        self.parent.sew = StatEditW(self.parent)
        self.parent.layout.addWidget(self.parent.sew)
        self.parent.sew.show()
        self.close()

    def setAttribs(self):
        for i in self.sDict:
            if self.sDict[i].aSet.isChecked() is False:
                MW.statusBar().showMessage('SET ALL ATTRIBUTES FIRST')
                return

        self.hide()
        print(str(self.aDict))
        for i in self.aDict:
            self.parent.PC.setAttrib(i, int(self.aDict[i]))
        print(self.parent.PC)
        rs.add_bonuses(self.parent.PC)
        rs.modifier_assign(self.parent.PC)
        self.parent.cdw = CharDisplayW(self.parent)
        self.parent.layout.addWidget(self.parent.cdw)
        self.parent.cdw.show()
        self.close()

    def autoAttribs(self):

        self.hide()
        print(str(self.aDict))
        rs.auto_assign(self.parent.PC)
        rs.add_bonuses(self.parent.PC)
        rs.modifier_assign(self.parent.PC)
        self.parent.cdw = CharDisplayW(self.parent)
        self.parent.layout.addWidget(self.parent.cdw)
        self.parent.cdw.show()
        self.close()


class CharDisplayW(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.aDict = {}

        self.initUI()

    def initUI(self):

        self.char = self.parent.PC
        self.attribs = self.char.getAttribDict()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.cName = QLabel(self.char.getName())
        self.grid.addWidget(self.cName, 0, 0)
        self.cRace = QLabel(self.char.getRace())
        self.grid.addWidget(self.cRace, 1, 0)
        self.cRole = QLabel(self.char.getRole())
        self.grid.addWidget(self.cRole, 2, 0)

        i = 0
        for k, v in self.attribs.items():
            self.aDict[k] = QLabel(str(k) + ": " + str(v))
            self.grid.addWidget(self.aDict[k], i, 1)
            i += 1

        self.cHP = QLabel("Hitpoints: " + str(self.char.getHitpoints()))
        self.grid.addWidget(self.cHP, i+1, 1)

#        self.bkBtn = QPushButton("Back")
#        self.bkBtn.clicked.connect(self.goBack)
#        self.grid.addWidget(self.bkBtn, 3, 0)

        self.setLayout(self.grid)
        self.show()

#    def goBack(self):
#        self.hide()
#        self.parent.saw = StatAssignW(self.parent)
#        self.parent.layout.addWidget(self.parent.saw)
#        self.parent.saw.show()
#        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MW = MainW()
    sys.exit(app.exec_())
