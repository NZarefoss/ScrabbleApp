import datetime
import os
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

Window.size = (450, 800)
Window.add_widget(Image(source = 'background.jpg', size = Window.size, allow_stretch = True, keep_ratio = False), canvas = 'before')

class GameData:
    def __init__(self):
        self.turn = 0
        self.teamNames = []
        self.teamScores = []
        self.turnScores = []
        self.turnWords = []

    def setTeamNames(self, teamNames):
        self.teamNames = teamNames

    def log(self):
        teams = ''
        for t in self.teamNames:
            teams += (t + ' ')

        scores = ''
        for s in self.teamScores:
            scores += (str(s) + ' ')

        turnScores = ''
        for s in self.turnScores:
            turnScores += (str(s) + ' ')
        
        turnWords = ''
        for w in self.turnWords:
            turnWords += (w + ' ')
        
        logData = teams + '\n' + scores + '\n' + turnScores + '\n' + turnWords
        return logData


    def nextTurn(self, score, word):
        self.turnScores.append(score)
        self.turnWords.append(word)

        self.teamScores[self.turn] += score

        if self.turn < (len(self.teamNames) - 1):
            self.turn += 1
        else:
            self.turn = 0


class HomePage(FloatLayout):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)

        self.teamCount = 2
        self.nameList = []

        self.teamNames = Popup(title = 'Enter Team Names', title_align = 'center', title_size = 30, separator_color = [150, 0, 0, 1], size_hint_x = .8, pos_hint = {'center_x': .5, 'center_y': .5}, auto_dismiss = False)

        self.logo = Image(source = 'scrabbleLogo.png', size_hint = (.8, .325), pos_hint = {'center_x': .5, 'top': .98})

        self.subHead = Label(text = 'Select Number of Teams:', font_size = 30, pos_hint = {'center_x': .5, 'y': .555}, size_hint = (.7, .15))

        self.numButtons = BoxLayout(orientation = 'horizontal', spacing = 15, size_hint = (.8, .2), pos_hint = {'center_x': .5, 'y': .38})

        self.two = ToggleButton(text = '2', font_size = 50, group = 'numbers', state = 'down', allow_no_selection = False, background_color = '#660000', on_press = self.setTeamCount)
        self.three = ToggleButton(text = '3', font_size = 50, group = 'numbers', allow_no_selection = False, background_color = '#660000', on_press = self.setTeamCount)
        self.four = ToggleButton(text = '4', font_size = 50, group = 'numbers', allow_no_selection = False, background_color = '#660000', on_press = self.setTeamCount)
        
        self.numButtons.add_widget(self.two)
        self.numButtons.add_widget(self.three)
        self.numButtons.add_widget(self.four)

        self.startButton = Button(text = 'Start Game', font_size = 50, background_color = '#660000', size_hint = (.8, .15), pos_hint = {'center_x': .5, 'y': .215}, on_release = self.startGame)
        
        self.loggedGamesButton = Button(text = 'Logged Games',  font_size = 50, background_color = '#660000', size_hint = (.8, .15), pos_hint = {'center_x': .5, 'y': .05}, on_release = self.loggedGames)

        self.add_widget(self.logo)
        self.add_widget(self.subHead)
        self.add_widget(self.numButtons)
        self.add_widget(self.startButton)
        self.add_widget(self.loggedGamesButton)

    def setTeamCount(self, instance):
        self.teamCount = int(instance.text)

    def startGame(self, instance):
        while len(self.nameList) < self.teamCount:
            self.nameList.append(TextInput(multiline = False, halign = 'center', font_size = 25))

        for t in self.nameList:
            label = Label(text = ('Team ' + str(self.nameList.index(t) + 1) + ': '), font_size = 25)
            GAME.namePage.container.add_widget(label)
            GAME.namePage.container.add_widget(t)

        GAME.screens.current = 'NamePage'
        

    def loggedGames(self, instance):
        GAME.screens.current = 'LogPage'
        
    
class NamePage(FloatLayout):
    def __init__(self, **kwargs):
        super(NamePage, self).__init__(**kwargs)

        self.title = Label(text = 'Enter Team Names', font_size = 50, pos_hint = {'center_x': .5, 'top': .95}, size_hint = (1, .1))

        self.container = GridLayout(cols = 1, row_default_height = 45, row_force_default = True, pos_hint = {'center_x': .5, 'top': .825}, size_hint = (.5, None))

        self.contButton = Button(text = 'Start', font_size = 50, size_hint = (.445, .125), pos_hint = {'x': .505, 'y': .05}, on_release = self.toGame, background_color = '#660000')

        self.backButton = Button(text = 'Back', font_size = 50, size_hint = (.445, .125), pos_hint = {'right': .495, 'y': .05}, on_release = self.goBack, background_color = '#660000')

        self.add_widget(self.title)
        self.add_widget(self.container)
        self.add_widget(self.contButton)
        self.add_widget(self.backButton)

    def toGame(self, instance):
        game = GameData()
        for t in GAME.homePage.nameList:
            name = t.text
            name = name.strip()

            if len(name) == 0:
                name = 'Team_' + str(GAME.homePage.nameList.index(t) + 1)
            
            game.teamNames.append(name)
            game.teamScores.append(0)
        
        GAME.gameData = game

        GAME.gamePage.update()
        GAME.screens.current = 'GamePage'

    def goBack(self, instance):
        self.container.clear_widgets()
        GAME.homePage.nameList = []
        GAME.screens.current = 'HomePage'

class OverviewPage(FloatLayout):
    def __init__(self, **kwargs):
        super(OverviewPage, self).__init__(**kwargs)

        self.size_hint = (1, 1)

        self.title = Label(text = 'Game Overview',underline = True, font_size = 50, size_hint = (.7, .15), pos_hint = {'center_x': .5, 'top': 1})

        self.heading = GridLayout(cols = 3, row_default_height = 30, row_force_default = True, pos_hint = {'center_x': .5, 'top': .86}, size_hint_x = .95)

        self.turnHead = Label(text = 'Turn', font_size = 25, size_hint_x = .3)
        self.scoreHead = Label(text = 'Score', font_size = 25, size_hint_x = .3)
        self.wordHead = Label(text = 'Word(s) Played', font_size = 25)

        self.heading.add_widget(self.turnHead)
        self.heading.add_widget(self.scoreHead)
        self.heading.add_widget(self.wordHead)

        self.scroller = ScrollView(size_hint = (.95, .69), pos_hint = {'center_x': .5, 'y': .125}, do_scroll = (False, True))

        self.scrollGrid = GridLayout(cols = 3, size_hint_y = None, row_default_height = 30, row_force_default = True)

        self.scroller.add_widget(self.scrollGrid)

        self.backButton = Button(text = 'Back to Game', size_hint = (.8, .1), pos_hint = {'center_x': .5, 'y': .015}, on_release = self.toGame, background_color = '#660000', font_size = 45)

        self.add_widget(self.title)
        self.add_widget(self.heading)
        self.add_widget(self.scroller)
        self.add_widget(self.backButton)

    def toGame(self, instance):
        GAME.screens.current = 'GamePage'

    def update(self):
        self.scrollGrid.clear_widgets()

        i = 0

        while i < len(GAME.gameData.turnScores):
            self.scrollGrid.add_widget(Label(text = str((i + 1)), size_hint_x = .3, font_size = 23))
            self.scrollGrid.add_widget(Label(text = str(GAME.gameData.turnScores[i]), font_size = 23, size_hint_x = .3))
            self.scrollGrid.add_widget(Label(text = str(GAME.gameData.turnWords[i]), font_size = 23))
            i += 1
        
        self.scrollGrid.bind(minimum_height = self.scrollGrid.setter('height'))


class EditTurnPage(FloatLayout):
    def __init__(self, **kwargs):
        super(EditTurnPage, self).__init__(**kwargs)

        self.size_hint = (1, 1)

        self.turnEditor = Popup(title = 'Enter New Turn Data', title_align = 'center', title_size = 30, separator_color = [150, 0, 0, 1], size_hint = (.8, .3), pos_hint = {'center_x': .5, 'center_y': .5}, auto_dismiss = True)

        self.container = GridLayout(cols = 1, spacing = 2)
    
        self.inputs = GridLayout(cols = 2, spacing = 5, padding = [10, 10], row_default_height = 50, row_force_default = True)

        self.pointsIn = TextInput(multiline = False, input_filter = 'int', padding = [10, 10], font_size = 20, size_hint_x = None, width = 100, hint_text = 'Score', halign = 'center')
        self.wordIn = TextInput(multiline = False, padding = [10, 10],font_size = 20, hint_text = 'Word(s)', halign = 'center')

        self.inputs.add_widget(self.pointsIn)
        self.inputs.add_widget(self.wordIn)

        self.confirmButton = Button(text = 'Confirm', on_release = self.editTurn, background_color = '#660000', font_size = 45)

        self.container.add_widget(self.inputs)
        self.container.add_widget(self.confirmButton)

        self.turnEditor.content = self.container

        self.title = Label(text = 'Game Overview',underline = True, font_size = 50, size_hint = (.7, .15), pos_hint = {'center_x': .5, 'top': 1})

        self.heading = GridLayout(cols = 3, row_default_height = 30, row_force_default = True, pos_hint = {'center_x': .5, 'top': .86}, size_hint_x = .95)

        self.turnHead = Label(text = 'Turn', font_size = 25, size_hint_x = .3)
        self.scoreHead = Label(text = 'Score', font_size = 25, size_hint_x = .3)
        self.wordHead = Label(text = 'Word(s) Played', font_size = 25)

        self.heading.add_widget(self.turnHead)
        self.heading.add_widget(self.scoreHead)
        self.heading.add_widget(self.wordHead)

        self.scroller = ScrollView(size_hint = (.95, .59), pos_hint = {'center_x': .5, 'y': .225}, do_scroll = (False, True))

        self.scrollGrid = GridLayout(cols = 3, size_hint_y = None, row_default_height = 30, row_force_default = True)

        self.scroller.add_widget(self.scrollGrid)

        self.turnLabel = Label(text = 'Turn: ', valign = 'bottom', halign = 'center', font_size = 30, size_hint = (.2, .1), pos_hint = {'x': .1, 'y': .105})

        self.turnSelect = TextInput(multiline = False, input_filter = 'int', padding = [10, 10], font_size = 30, halign = 'center', size_hint = (.2, .075), pos_hint = {'x': .3, 'y': .12})

        self.submitButton = Button(text = 'Submit', size_hint = (.375, .075), padding = [5, 5], font_size = 35, pos_hint = {'right': .9, 'y': .12}, on_release = self.turnEditor.open, background_color = '#660000')

        self.backButton = Button(text = 'Back to Game', size_hint = (.8, .1), font_size = 45, pos_hint = {'center_x': .5, 'y': .015}, on_release = self.toGame, background_color = '#660000')

        self.add_widget(self.title)
        self.add_widget(self.heading)
        self.add_widget(self.scroller)
        self.add_widget(self.backButton)
        self.add_widget(self.turnLabel)
        self.add_widget(self.turnSelect)
        self.add_widget(self.submitButton)

    def toGame(self, instance):
        GAME.screens.current = 'GamePage'
    
    def editTurn(self, instance):
        turn = int(self.turnSelect.text) - 1
        score = int(self.pointsIn.text)
        word = self.wordIn.text

        GAME.gameData.turnScores[turn] = score
        GAME.gameData.turnWords[turn] = word

        self.update()



    def update(self):
        self.scrollGrid.clear_widgets()

        self.turnSelect.text = ''
        self.pointsIn.text = ''
        self.wordIn.text = ''

        i = 0

        while i < len(GAME.gameData.turnScores):
            self.scrollGrid.add_widget(Label(text = str((i + 1)), size_hint_x = .3, font_size = 23))
            self.scrollGrid.add_widget(Label(text = str(GAME.gameData.turnScores[i]), font_size = 23, size_hint_x = .3))
            self.scrollGrid.add_widget(Label(text = str(GAME.gameData.turnWords[i]), font_size = 23))
            i += 1
        
        self.scrollGrid.bind(minimum_height = self.scrollGrid.setter('height'))

class GamePage(FloatLayout):
    def __init__(self, **kwargs):
        super(GamePage, self).__init__(**kwargs)

        self.size_hint = (1, 1)
        self.empty = True
        self.scoreFont = 'chawp.ttf'

        self.verification = Popup(title = 'Are you sure?', title_align = 'center', title_size = 30, separator_color = [150, 0, 0, 1], size_hint = (.7, .3), pos_hint = {'center_x': .5, 'center_y': .5}, auto_dismiss = False)
        self.vButtons = BoxLayout(orientation = 'vertical', padding = [5, 5], spacing = 2)
        self.vYes = Button(text = 'Yes', on_release = self.exchangeTiles, background_color = '#660000', font_size = 45)
        self.vNo = Button(text = 'No', on_release = self.verification.dismiss, background_color = '#660000', font_size = 45)
        self.vButtons.add_widget(self.vYes)
        self.vButtons.add_widget(self.vNo)
        self.verification.add_widget(self.vButtons)

        self.scoreboardImage = Image(source = 'chalkboard.png', size_hint = (.8, .45), pos_hint = {'top': .95, 'center_x': .5}, allow_stretch = True, keep_ratio = False)

        self.add_widget(self.scoreboardImage)

        self.saveWindow = Popup(title = 'Log Game Data?', title_align = 'center', title_size = 30, separator_color = [150, 0, 0, 1], size_hint = (.7, .3), pos_hint = {'center_x': .5, 'center_y': .5}, auto_dismiss = False)

        self.quitWindow = Popup(title = 'Do you want to quit?', title_align = 'center', title_size = 30, separator_color = [150, 0, 0, 1], size_hint = (.7, .3), pos_hint = {'center_x': .5, 'center_y': .5}, auto_dismiss = False)

        self.scoreboard = GridLayout(size_hint = (.6, .35), pos_hint = {'top': .91, 'center_x': .5}, cols = 2, rows = 2, spacing = 10, row_default_height = 125, row_force_default = True)

        for t in GAME.gameData.teamNames:
            team = BoxLayout(orientation = 'vertical')
            name = Label(text = t, font_size = 25, halign = 'center', font_name = 'chawp.ttf')
            score = Label(text = str(GAME.gameData.teamScores[GAME.gameData.teamNames.index(t)]), font_size = 60, halign = 'center', font_name = 'chawp.ttf')

            team.add_widget(name)
            team.add_widget(score)
            self.scoreboard.add_widget(team)

        self.add_widget(self.scoreboard)

        self.inputs = GridLayout(cols = 2, size_hint = (.8, None), pos_hint = {'center_x': .5, 'top': .49}, spacing = 5, padding = [10, 10], row_default_height = 50, row_force_default = True)

        self.pointsIn = TextInput(multiline = False, input_filter = 'int', padding = [10, 10], font_size = 20, size_hint_x = None, width = 100, hint_text = 'Score', halign = 'center')
        self.wordIn = TextInput(multiline = False, padding = [10, 10],font_size = 20, hint_text = 'Word(s)', halign = 'center')

        self.inputs.add_widget(self.pointsIn)
        self.inputs.add_widget(self.wordIn)

        self.add_widget(self.inputs)

        self.gameButtons = BoxLayout(orientation = 'vertical', padding = [5, 5], spacing = 5, size_hint = (.85, .375), pos_hint = {'center_x': .5, 'y': .025})

        self.nextTurnButton = Button(text = 'Next Turn', font_size = 30, on_release = self.nextTurn, background_color = '#660000')

        self.smallButtons = BoxLayout(orientation = 'horizontal', spacing = 5)

        self.tradeButton = Button(text = 'Trade Tiles', font_size = 30, on_release = self.verification.open, background_color = '#660000')
        self.editButton = Button(text = 'Edit Turn', font_size = 30, on_press = self.editTurn, background_color = '#660000')
        self.smallButtons.add_widget(self.editButton)
        self.smallButtons.add_widget(self.tradeButton)

        self.overviewButton = Button(text = 'Overview', font_size = 30, on_release = self.goToOverview, background_color = '#660000')

        self.quitButton = Button(text = 'Fig Out', font_size = 30, on_release = self.quitGame, background_color = '#cc0000')

        self.gameButtons.add_widget(self.nextTurnButton)
        self.gameButtons.add_widget(self.smallButtons)
        self.gameButtons.add_widget(self.overviewButton)
        self.gameButtons.add_widget(self.quitButton)

        self.add_widget(self.gameButtons)
    
    def exchangeTiles(self, instance):
        self.verification.dismiss()

        score = 0
        word = '*EXCHANGED*'

        GAME.gameData.nextTurn(score, word)

        self.update()
    
    def editTurn(self, instance):
        GAME.editTurnPage.update()
        GAME.screens.current = 'EditTurnPage'
    
    def goToOverview(self, instance):
        GAME.overviewPage.update()
        GAME.screens.current = 'OverviewPage'

    def update(self):

        self.scoreboard.clear_widgets()

        self.pointsIn.text = ''
        self.wordIn.text = ''

        for t in GAME.gameData.teamNames:
            team = BoxLayout(orientation = 'vertical')
            name = Label(text = t, font_size = 25, halign = 'center', font_name = 'chawp.ttf')
            score = Label(text = str(GAME.gameData.teamScores[GAME.gameData.teamNames.index(t)]), font_size = 60, halign = 'center', font_name = 'chawp.ttf')

            team.add_widget(name)
            team.add_widget(score)
            self.scoreboard.add_widget(team)


    def nextTurn(self, instance):
        score = self.pointsIn.text.strip()
        word = self.wordIn.text.strip()

        if len(score) > 0 and len(word) > 0:
            GAME.gameData.nextTurn(int(score), word)

            self.update()
        
        else:
            Popup(title = 'Invalid Turn', size_hint = (.5, .2), pos_hint = {'center_x': .5, 'center_y': .5}, separator_color = [150, 0, 0, 1], title_align = 'center', auto_dismiss = True).open()
            self.update()
    
    

    def saveGame(self, instance):
        self.quitWindow.dismiss()

        saveButtons = BoxLayout(orientation = 'vertical', padding = [5, 5], spacing = 2)
        yesButton = Button(text = 'Yes', on_release = self.logData, background_color = '#660000', font_size = 45)
        noButton = Button(text = 'No', on_release = self.exitGame, background_color = '#660000', font_size = 45)

        saveButtons.add_widget(yesButton)
        saveButtons.add_widget(noButton)

        self.saveWindow.content = saveButtons

        self.saveWindow.open()

    def quitGame(self, instance):
        quitButtons = BoxLayout(orientation = 'vertical', padding = [5, 5], spacing = 2)
        yesButton = Button(text = 'Yes', on_release = self.saveGame, background_color = '#660000', font_size = 45)
        noButton = Button(text = 'No', on_release = self.quitWindow.dismiss, background_color = '#660000', font_size = 45)
        quitButtons.add_widget(yesButton)
        quitButtons.add_widget(noButton)

        self.quitWindow.content = quitButtons

        self.quitWindow.open()
    
    def logData(self, instance):
        x = datetime.datetime.now()
        thisYear = x.strftime('%Y')
        thisDay = x.strftime('%d')
        thisMonth = x.strftime('%m')
        thisHour = x.strftime('%H')
        thisMinute = x.strftime('%M')
        thisSecond = x.strftime('%S')

        fileName = 'Data/' + thisYear + '-' + thisDay + '-' + thisMonth + '_' + thisHour + '-' + thisMinute + '-' + thisSecond + '.txt'

        if len(os.listdir('Data/')) > 19:
            os.remove(os.listdir('Data/')[0])

        dataFile = open(fileName, 'w')
        dataFile.write(GAME.gameData.log())
        dataFile.close()

        self.saveWindow.dismiss()
        GAME.homePage.nameList = []
        GAME.namePage.container.clear_widgets()
        GAME.screens.current = 'HomePage'

    def exitGame(self, instance):
        self.saveWindow.dismiss()
        GAME.homePage.nameList = []
        GAME.namePage.container.clear_widgets()
        GAME.screens.current = 'HomePage'
    
class Scoreboard(FloatLayout):
    def __init__(self, date, data, **kwargs):
        super(Scoreboard, self).__init__(**kwargs)

        self.date = date
        self.data = data

        self.dateLabel = Label(text = self.date, size_hint = (1, .1), pos_hint = {'center_x': .5, 'top': .9}, font_size = 40, font_name = 'chawp.ttf')

        self.scores = GridLayout(cols = 2, rows = 2, size_hint = (.8, .65), pos_hint = {'center_x': .5, 'top': .75}, row_force_default = True, row_default_height = 90)

        for n in self.data[0]:
            s = self.data[1][self.data[0].index(n)]

            scoreBox = BoxLayout(orientation = 'vertical')
            team = Label(text = n, font_name = 'chawp.ttf', font_size = 30)
            score = Label(text = s, font_name = 'chawp.ttf', font_size = 40)

            scoreBox.add_widget(team)
            scoreBox.add_widget(score)

            self.scores.add_widget(scoreBox)

        self.add_widget(self.dateLabel)
        self.add_widget(self.scores)

        

class LogGameData(FloatLayout):
    def __init__(self, file, pgNum, **kwargs):
        super(LogGameData, self).__init__(**kwargs)

        self.pageNumber = pgNum

        self.file = file
        self.path = 'Data/' + file

        self.gameDate = self.file.split('_')[0].split('-')

        self.logData = []

        for l in open(self.path, 'r').readlines():
            line = l.split()
            if line[-1] == '\n':
                lineInfo = line[:-1]
            else:
                lineInfo = line
            
            self.logData.append(line)

        self.dateText = self.gameDate[2] + '/' + self.gameDate[1] + '/' + self.gameDate[0]

        self.scoreboard = Scoreboard(self.dateText, self.logData, size_hint = (.7, .35), pos_hint = {'center_x': .5, 'top': .97})
        self.add_widget(Image(source = 'chalkboard.png', allow_stretch = True, keep_ratio = False, pos_hint = self.scoreboard.pos_hint, size_hint = self.scoreboard.size_hint), canvas = 'before')

        self.turnListHeader = GridLayout(cols = 3, row_default_height = 25, row_force_default = True, pos_hint = {'center_x': .55, 'top': .615}, size_hint_x = .7)

        self.turnListHeader.add_widget(Label(text = 'Turn', size_hint_x = .2))
        self.turnListHeader.add_widget(Label(text = 'Score', size_hint_x = .2))
        self.turnListHeader.add_widget(Label(text = 'Word(s)', size_hint_x = .6))

        self.turnScroll = ScrollView(size_hint = (.7, .42), pos_hint = {'center_x': .55, 'y': .16}, do_scroll = (False, True))

        self.turnList = GridLayout(cols = 3, row_default_height = 20, row_force_default = True, size_hint = (1, None))

        i = 0

        while i < len(self.logData[2]):
            turn = str((i + 1))
            score = str(self.logData[2][i])
            word = str(self.logData[3][i])

            self.turnList.add_widget(Label(text = turn, size_hint_x = .2))
            self.turnList.add_widget(Label(text = score, size_hint_x = .2))
            self.turnList.add_widget(Label(text = word, size_hint_x = .6))
            i += 1

        self.turnList.bind(minimum_height = self.turnList.setter('height'))
        self.turnScroll.add_widget(self.turnList)


        self.add_widget(self.scoreboard)
        self.add_widget(self.turnScroll)
        self.add_widget(self.turnListHeader)

class LogPageLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(LogPageLayout, self).__init__(**kwargs)

        self.gameList = []
        self.currentGame = 0
        

        for file in os.listdir('Data/'):
            self.gameList.append(LogGameData(file, (len(self.gameList) + 1)))

        if len(self.gameList) > 0:
            self.pButton = Button(text = '<', size_hint = (.1, .35), pos_hint = {'x': .03, 'top': .97}, on_release = self.prevGame, background_color = '#660000', font_size = 50)

            self.nButton = Button(text = '>', size_hint = (.1, .35), pos_hint = {'right': .97, 'top': .97}, on_release = self.nextGame, background_color = '#660000', font_size = 50)

            self.homeButton = Button(text = 'Back to Home', pos_hint = {'center_x': .5, 'y': .01}, size_hint = (.7, .1), on_release = self.toHome, background_color = '#660000', font_size = 40)

            self.pageNumber = Label(text = (str(self.currentGame + 1) + ' / ' + str(len(self.gameList))), size_hint = (.025, .05), pos_hint = {'center_x': .5, 'y': .11})

            if len(self.gameList) > 0:
                self.displayedGame = self.gameList[0]
                self.add_widget(self.displayedGame)

            self.add_widget(self.pButton)
            self.add_widget(self.nButton)
            self.add_widget(self.homeButton)
            self.add_widget(self.pageNumber)
        
        else:
            self.empty1 = Label(text = 'No Games', font_size = 50, size_hint = (1, .2), pos_hint = {'center_x': .5, 'y': .6})
            self.empty2 = Label(text = 'Available', font_size = 50, size_hint = (1, .2), pos_hint = {'center_x': .5, 'top': .6})

            self.homeButton = Button(text = 'Back to Home', pos_hint = {'center_x': .5, 'y': .05}, size_hint = (.8, .2), on_release = self.toHome, background_color = '#660000', font_size = 40)

            self.add_widget(self.empty1)
            self.add_widget(self.empty2)
            self.add_widget(self.homeButton)

    def prevGame(self, instance):
        if self.currentGame > 0:
            self.currentGame -= 1
        
        self.clear_widgets([self.displayedGame, self.pageNumber])
        self.displayedGame = self.gameList[self.currentGame]
        self.pageNumber.text = (str(self.currentGame + 1) + ' / ' + str(len(self.gameList)))
        self.add_widget(self.displayedGame)
        self.add_widget(self.pageNumber)

    def nextGame(self, instance):
        if self.currentGame < len(self.gameList) - 1:
            self.currentGame += 1

        self.clear_widgets([self.displayedGame, self.pageNumber])
        self.displayedGame = self.gameList[self.currentGame]
        self.pageNumber.text = (str(self.currentGame + 1) + ' / ' + str(len(self.gameList)))
        self.add_widget(self.displayedGame)
        self.add_widget(self.pageNumber)

        
    def toHome(self, instance):
        GAME.screens.current = 'HomePage'


class Scrabble(App):
    def build(self):
        self.gameData = GameData()

        self.screens = ScreenManager()

        self.homePage = HomePage()
        screen = Screen(name = 'HomePage')
        screen.add_widget(self.homePage)
        self.screens.add_widget(screen)

        self.namePage = NamePage()
        screen = Screen(name = 'NamePage')
        screen.add_widget(self.namePage)
        self.screens.add_widget(screen)

        self.gamePage = GamePage()
        screen = Screen(name = 'GamePage')
        screen.add_widget(self.gamePage)
        self.screens.add_widget(screen)

        self.logPage = LogPageLayout()
        screen = Screen(name = 'LogPage')
        screen.add_widget(self.logPage)
        self.screens.add_widget(screen)

        self.overviewPage = OverviewPage()
        screen = Screen(name = 'OverviewPage')
        screen.add_widget(self.overviewPage)
        self.screens.add_widget(screen)

        self.editTurnPage = EditTurnPage()
        screen = Screen(name = 'EditTurnPage')
        screen.add_widget(self.editTurnPage)
        self.screens.add_widget(screen)


        return self.screens



if __name__ == '__main__':
    GAME = Scrabble()
    GAME.run()