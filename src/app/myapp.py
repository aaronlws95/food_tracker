import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, \
                            QInputDialog, QLineEdit, QFileDialog, QLabel, \
                            QAction, qApp, QPushButton, QGridLayout, QSpacerItem, \
                            QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon, QFont
import json
from src.app.widgets import ClientInfoWidget, MealInfoWidget

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.client_info = {}
        self.meal_info = {}
        self.meal_day = 'Monday'
        self.meal_type = 'Lunch'
        self.initUI()

    def initUI(self):
        self.setupWindow('Meal Tracker', 0, 0, 960, 720)
        self.setupMenuBar()
        self.statusBar()
        self.setupLayout()
        self.setCentralWidget(self.central_widget)
        self.show()

    def getInitLayout(self):
        init_layout = QGridLayout()
        button = QPushButton('Client', self)
        button.clicked.connect(self.makeShowClientInfo())
        init_layout.addWidget(button, 0, 0, 1, QSizePolicy.Minimum)
        button = QPushButton('Meal', self)
        button.clicked.connect(self.makeShowMealInfo(meal_day=self.meal_day, meal_type=self.meal_type))
        init_layout.addWidget(button, 0, 1, 1, QSizePolicy.Minimum)
        return init_layout

    def getMealButtonLayout(self):
        meal_type_layout = QGridLayout()
        meals = ['Breakfast', 'Lunch', 'Snack', 'Dinner', 'Supper']
        pos_i = 0
        pos_j = 0
        for m in meals:
            button = QPushButton(m, self)
            button.clicked.connect(self.makeShowMealInfo(meal_day=self.meal_day, meal_type=m))
            pos_j += 1
            meal_type_layout.addWidget(button, pos_i, pos_j, 1, 1)
        meal_days_layout = QGridLayout()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pos_i += 1
        pos_j = 0
        for d in days:
            button = QPushButton(d, self)
            button.clicked.connect(self.makeShowMealInfo(meal_day=d, meal_type=self.meal_type))
            pos_j += 1
            meal_days_layout.addWidget(button, pos_i, pos_j, 1, 1)
        meal_button_layout = QGridLayout()
        meal_button_layout.addLayout(meal_type_layout, 0, 0)
        meal_button_layout.addLayout(meal_days_layout, 1, 0)
        return meal_button_layout

    def setupLayout(self):
        cur_layout = self.getInitLayout()
        cur_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.central_widget = QWidget()
        self.central_widget.setLayout(cur_layout)

    def setupMenuBar(self):
        # Load Client
        loadClientAct = QAction('&Load Client', self)
        loadClientAct.setShortcut('Ctrl+L')
        loadClientAct.setStatusTip('Load Client Info')
        loadClientAct.triggered.connect(self.makeShowClientInfo(load=True))

        # Save Client
        saveClientAct = QAction('&Save Client', self)
        saveClientAct.setShortcut('Ctrl+S')
        saveClientAct.setStatusTip('Save Client Info')
        saveClientAct.triggered.connect(self.saveClientInfo)

        # Load Meal
        loadMealAct = QAction('&Load Meal', self)
        loadMealAct.setShortcut('Ctrl+K')
        loadMealAct.setStatusTip('Load Meal Info')
        loadMealAct.triggered.connect(self.makeShowMealInfo(self.meal_day, self.meal_type, load=True))

        # Save Meal
        saveMealAct = QAction('&Save Meal', self)
        saveMealAct.setShortcut('Ctrl+D')
        saveMealAct.setStatusTip('Save Meal Info')
        saveMealAct.triggered.connect(self.saveMealInfo)

        # Exit
        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Quit Application')
        exitAct.triggered.connect(qApp.exit)

        fileMenu = self.menuBar().addMenu('&File')

        fileMenu.addAction(loadClientAct)
        fileMenu.addAction(saveClientAct)
        fileMenu.addAction(loadMealAct)
        fileMenu.addAction(saveMealAct)
        fileMenu.addAction(exitAct)


    def setupWindow(self, title, left, top, width, height):
        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height)
        self.move(60, 15)

    def saveFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,'Save File', '','Json Files (*.json)', options=options)
        return fileName

    def saveClientInfo(self):
        fileName = self.saveFileNameDialog()
        if fileName.split('.')[-1] !=  'json':
            fileName += '.json'
        with open(fileName, 'w') as f:
            json.dump(self.client_info, f)

    def saveMealInfo(self):
        fileName = self.saveFileNameDialog()
        if fileName.split('.')[-1] !=  'json':
            fileName += '.json'
        with open(fileName, 'w') as f:
            json.dump(self.meal_info, f)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,'Open File', '','Json Files (*.json)', options=options)
        return fileName

    def readClientJson(self):
        fileName = self.openFileNameDialog()
        if fileName.split('.')[-1] == 'json':
            with open(fileName, 'r') as f:
                self.client_info = json.load(f)

    def readMealJson(self):
        fileName = self.openFileNameDialog()
        if fileName.split('.')[-1] == 'json':
            with open(fileName, 'r') as f:
                self.meal_info = json.load(f)

    def makeShowClientInfo(self, load=False):
        def showClientInfo():
            if load or not self.client_info:
                self.readClientJson()
            self.central_widget = ClientInfoWidget(self.getInitLayout(), self.client_info)
            self.setCentralWidget(self.central_widget)
        return showClientInfo

    def makeShowMealInfo(self, meal_day, meal_type, load=False):
        def showMealInfo():
            self.meal_day = meal_day
            self.meal_type = meal_type
            if load or not self.meal_info:
                self.readMealJson()
            self.central_widget = MealInfoWidget(self.getInitLayout(), self.getMealButtonLayout(), self.meal_info, meal_day, meal_type)
            self.setCentralWidget(self.central_widget)
        return showMealInfo


