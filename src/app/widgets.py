from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, \
                            QInputDialog, QLineEdit, QFileDialog, QLabel, \
                            QAction, qApp, QPushButton, QGridLayout, QSpacerItem, \
                            QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon, QFont

class ClientInfoWidget(QWidget):
    def __init__(self, init_layout, client_info):
        super().__init__()
        self.init_layout = init_layout
        self.client_info = client_info
        self.initUI()

    def initUI(self):
        new_layout = QGridLayout()
        pos_i = 0
        for k, v in self.client_info.items():
            new_layout.addWidget(QLabel('%s : ' %k), pos_i, 0, 1, 1)
            textbox = QLineEdit(self)
            textbox.setText(str(v))
            textbox.textChanged.connect(self.makeUpdateClientInfo(k))
            new_layout.addWidget(textbox, pos_i, 1, 1, 2)
            pos_i += 1

        main_layout = QGridLayout()
        main_layout.addLayout(self.init_layout, 0, 0)
        main_layout.addLayout(new_layout, 1, 0)
        main_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)

    def makeUpdateClientInfo(self, key):
        def updateClientInfo(text):
            self.client_info[key] = text
        return updateClientInfo

class MealInfoWidget(QWidget):
    def __init__(self, init_layout, meal_button_layout, meal_info, meal_day, meal_type):
        super().__init__()
        self.init_layout = init_layout
        self.meal_button_layout = meal_button_layout

        self.meal_info = meal_info
        self.meal_day = meal_day
        self.meal_type = meal_type

        self.textboxes = []
        self.buttons = []
        self.button_layouts = []
        self.food_layouts = []
        self.food_layouts_rows = [] # last rows for each food item
        self.nutri_sum = []
        self.nutri_sum_label = []
        self.initUI()

    def initUI(self):

        self.overall_food_layout = QGridLayout()
        self.overall_food_layout.addLayout(self.init_layout, 0, 0)

        new_layout = QGridLayout()
        pos_i = 0
        label = QLabel('<b>%s</b>' %self.meal_day)
        label.setFont(QFont('Arial', 20))
        new_layout.addWidget(label, pos_i, 0, 1, 1)
        label = QLabel('<b>%s</b>' %self.meal_type)
        label.setFont(QFont('Arial', 20))
        new_layout.addWidget(label, pos_i, 1, 1, 1)
        pos_i += 1
        new_layout.addWidget(QLabel('<b>Food</b>'), pos_i, 0, 1, 1)
        new_layout.addWidget(QLabel('<b>Kcal</b>'), pos_i, 1, 1, 1)
        new_layout.addWidget(QLabel('<b>Protein</b>'), pos_i, 2, 1, 1)
        new_layout.addWidget(QLabel('<b>Fat</b>'), pos_i, 3, 1, 1)
        new_layout.addWidget(QLabel('<b>Carb</b>'), pos_i, 4, 1, 1)
        new_layout.addWidget(QLabel('<b>Fibre</b>'), pos_i, 5, 1, 1)
        self.overall_food_layout.addLayout(new_layout, 1, 0)

        self.food_pos_i = 2
        food_lst = self.meal_info[self.meal_day][self.meal_type]
        for i, f in enumerate(food_lst):
            self.addTextBox(f['Name'], i, 'Name', 0, 0, 0, 0)

            pos_i = 1
            for j, c in enumerate(f['Content']):
                pos_j = 0
                for k, v in c.items():
                    self.addTextBox(str(v), i, 'Content', j, k, pos_i, pos_j)
                    if k != 'Name':
                        val = float(v) if str(v) != '' else 0
                        self.nutri_sum[i][k] += val
                    pos_j += 1
                pos_i += 1

            for ind, (k, v) in enumerate(self.nutri_sum[i].items()):
                label = QLabel('<b>%s</b>' %str(v))
                self.nutri_sum_label[i][k] = label
                self.food_layouts[i].addWidget(label, 0, ind + 1, 1, 1)

            self.food_layouts_rows.append(pos_i - 1)
            self.overall_food_layout.addLayout(self.food_layouts[-1], self.food_pos_i, 0)
            self.food_pos_i += 1
            self.addAddandRemoveContentButton(i)

        self.spacer_item = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.overall_food_layout.addItem(self.spacer_item)

        button = QPushButton('Add Food', self)
        button.clicked.connect(self.makeAddFood(self.meal_day, self.meal_type))
        new_layout = QGridLayout()
        new_layout.addWidget(button, 0, 0, 1, 1)

        main_layout = QGridLayout()
        main_layout.addLayout(self.overall_food_layout, 0, 0)
        main_layout.addLayout(new_layout, 1, 0)
        main_layout.addLayout(self.meal_button_layout, 2, 0)

        self.setLayout(main_layout)

    def makeAddFood(self, meal_day, meal_type):
        def addFood():

            new_food_tmp = {
                'Name' : '',
                'Content' : [
                    {
                        'Name' : '',
                        'Kcal' : '',
                        'Protein' : '',
                        'Fat' : '',
                        'Carb' : '',
                        'Fibre' : '',
                    }
                ]
            }

            self.meal_info[meal_day][meal_type].append(new_food_tmp)

            self.addTextBox('', len(self.meal_info[meal_day][meal_type]) - 1, 'Name', 0, 0, 0, 0)

            pos_j = 0
            for k, _ in new_food_tmp['Content'][0].items():
                self.addTextBox('', len(self.meal_info[meal_day][meal_type]) - 1, 'Content', 0, k, 1, pos_j)
                pos_j += 1

            self.food_layouts_rows.append(1)

            self.overall_food_layout.addLayout(self.food_layouts[-1], self.food_pos_i , 0)
            self.food_pos_i += 1
            self.addAddandRemoveContentButton(len(self.meal_info[meal_day][meal_type]) - 1)

            self.overall_food_layout.removeItem(self.spacer_item)
            self.overall_food_layout.addItem(self.spacer_item)
        return addFood

    def makeDeleteFoodContent(self, meal_day, meal_type, i):
        def deleteFoodContent():
            for k, v in self.meal_info[meal_day][meal_type][i]['Content'][-1].items():
                if k != 'Name':
                    self.nutri_sum[i][k] = self.nutri_sum[i][k] - float(self.meal_info[meal_day][meal_type][i]['Content'][-1][k])
                    self.nutri_sum_label[i][k].setText('<b>%s</b>' %str(self.nutri_sum[i][k]))
            self.meal_info[meal_day][meal_type][i]['Content'] =  self.meal_info[meal_day][meal_type][i]['Content'][:-1]
            for col in range(6):
                if (self.food_layouts_rows[i], col) in self.textboxes[i]:
                    self.food_layouts[i].removeWidget(self.textboxes[i][(self.food_layouts_rows[i], col)])
                    self.textboxes[i][(self.food_layouts_rows[i], col)].deleteLater()
                    del self.textboxes[i][(self.food_layouts_rows[i], col)]
            self.food_layouts_rows[i] -= 1
            if self.food_layouts_rows[i] < 0 :
                self.button_layouts[i].removeWidget(self.buttons[i][0])
                self.button_layouts[i].removeWidget(self.buttons[i][1])
                self.buttons[i][0].deleteLater()
                self.buttons[i][1].deleteLater()
                del self.buttons[i]
        return deleteFoodContent

    def makeAddFoodContent(self, meal_day, meal_type, i):
        def addFoodContent():
            content = {
                'Name' : '',
                'Kcal' : '',
                'Protein' : '',
                'Fat' : '',
                'Carb' : '',
                'Fibre' : '',
            }
            self.meal_info[meal_day][meal_type][i]['Content'].append(content)
            self.food_layouts_rows[i] += 1
            pos_j = 0
            for k, v in content.items():
                self.addTextBox(str(v), i, 'Content', len(self.meal_info[meal_day][meal_type][i]['Content']) - 1, k, self.food_layouts_rows[i], pos_j)
                pos_j += 1
        return addFoodContent

    def makeUpdateMealInfo(self, meal_day, meal_type, i, name, j, k):
        def updateMealInfo(text):
            if name == 'Content':
                if k != 'Name':
                    if self.meal_info[meal_day][meal_type][i]['Content'][j][k] == '':
                        self.meal_info[meal_day][meal_type][i]['Content'][j][k] = 0
                    if text == '':
                        text = 0
                    self.nutri_sum[i][k] = self.nutri_sum[i][k] - float(self.meal_info[meal_day][meal_type][i]['Content'][j][k]) + float(text)
                    self.nutri_sum_label[i][k].setText('<b>%s</b>' %str(self.nutri_sum[i][k]))
                self.meal_info[meal_day][meal_type][i]['Content'][j][k] = text
            elif name == 'Name':
                self.meal_info[meal_day][meal_type][i]['Name'] = text
        return updateMealInfo

    def addTextBox(self, text, i, name, j, k, pos_i, pos_j):
        if name == 'Name':
            self.textboxes.append({})
            self.nutri_sum_label.append({'Kcal' : 0, 'Protein' : 0, 'Fat' : 0, 'Carb' : 0, 'Fibre' : 0})
            self.food_layouts.append(QGridLayout())
            self.nutri_sum.append({'Kcal' : 0, 'Protein' : 0, 'Fat' : 0, 'Carb' : 0, 'Fibre' : 0})
        textbox = QLineEdit(self)
        textbox.setText(text)
        textbox.textChanged.connect(self.makeUpdateMealInfo(self.meal_day, self.meal_type, i, name, j, k))
        # add widget to corresponding layout
        self.food_layouts[i].addWidget(textbox, pos_i, pos_j, 1, 1)
        # keep reference to widget
        self.textboxes[i][(pos_i, pos_j)] = textbox

    def addAddandRemoveContentButton(self, i):
        new_layout = QGridLayout()

        add_button = QPushButton('Add Content', self)
        add_button.clicked.connect(self.makeAddFoodContent(self.meal_day, self.meal_type, i))
        new_layout.addWidget(add_button, 0, 0, 1, QSizePolicy.Minimum)

        del_button = QPushButton('Delete Content', self)
        del_button.clicked.connect(self.makeDeleteFoodContent(self.meal_day, self.meal_type, i))
        new_layout.addWidget(del_button, 0, 1, 1, QSizePolicy.Minimum)

        self.button_layouts.append(new_layout)
        self.buttons.append([add_button, del_button])

        self.overall_food_layout.addLayout(new_layout, self.food_pos_i, 0)
        self.food_pos_i += 1