import sys
from src.mastermind import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget


class MastermindGame(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Mastermind Color Game')
        self.setGeometry(100, 100, 400, 300)

        self.initUI()

    def init_values(self):

        self.available_colors = [color for color in AVAILABLE_COLORS_POOL.value]
        self.selected_colors = select_distinct_colors()
        self.user_selected_colors = []
        self.total_attempts = 1

    def reset_values(self):

        self.init_values()
        self.message_label.setText("")
        self.updateLists() 



    def initUI(self):
        self.init_values()

        self.layout = QVBoxLayout()
        self.layout_color = QHBoxLayout()
        self.layout_label = QHBoxLayout()
    
        self.available_colors_label = QLabel("Available Colors")
        self.layout_label.addWidget(self.available_colors_label)

        self.available_colors_list = QListWidget()
        for color in self.available_colors:
            self.available_colors_list.addItem(color.name)
        self.layout_color.addWidget(self.available_colors_list)

        
        self.user_selected_colors_label = QLabel("Guess Colors")
        self.layout_label.addWidget(self.user_selected_colors_label)

        self.user_selected_colors_list = QListWidget()
        self.layout_color.addWidget(self.user_selected_colors_list)

        self.layout.addLayout(self.layout_label)
        self.layout.addLayout(self.layout_color)
        
        self.button_layout = QHBoxLayout()

        self.move_right_button = QPushButton("Move Right ->")
        self.move_right_button.clicked.connect(self.moveRight)
        self.button_layout.addWidget(self.move_right_button)

        self.move_left_button = QPushButton("<- Move Left")
        self.move_left_button.clicked.connect(self.moveLeft)
        self.button_layout.addWidget(self.move_left_button)

        self.layout.addLayout(self.button_layout)

        self.guess_count = QLabel("Guess Count: ")
        self.layout.addWidget(self.guess_count)

        self.number_of_attempts = QLabel("0")
        self.layout.addWidget(self.number_of_attempts)

        self.message_label = QLabel()
        self.layout.addWidget(self.message_label)

        self.setLayout(self.layout)

        self.button_layout1 = QHBoxLayout()

        self.reset_button = QPushButton('Restart Game')
        self.reset_button.clicked.connect(self.reset_values)
        self.button_layout1.addWidget(self.reset_button)
        
        self.submit_button = QPushButton('Submit Guess')
        self.submit_button.clicked.connect(self.checkGuess)
        self.button_layout1.addWidget(self.submit_button)
        
        self.layout.addLayout(self.button_layout1)

    def moveRight(self):
        selected_items = self.available_colors_list.selectedItems()
        for item in selected_items:
            color_name = item.text()
            color_enum = next((color for color in self.available_colors if color.name == color_name))

            self.available_colors.remove(color_enum)
            self.user_selected_colors.append(color_enum)

        self.updateLists()


    def moveLeft(self):
        selected_items = self.user_selected_colors_list.selectedItems()
        for item in selected_items:
            color = item.text()

            color_name = item.text()
            color_enum = next((color for color in self.user_selected_colors if color.name == color_name))

            self.user_selected_colors.remove(color_enum)
            self.available_colors.append(color_enum)

        self.updateLists()

    def updateLists(self):
        self.available_colors_list.clear()
        for color in self.available_colors:
            self.available_colors_list.addItem(color.name)

        self.user_selected_colors_list.clear()
        for color in self.user_selected_colors:
            self.user_selected_colors_list.addItem(color.name)


    def checkGuess(self):


        try:
            
            (progress, result) = play(self.total_attempts, self.selected_colors, self.user_selected_colors)

            match_string = ""

            if progress == WON:
                self.winUI()

            elif progress == LOST:
                self.looseUI()

            else:

                for match in result:
                    if match == EXACT:
                        match_string = match_string + "BLACK"+ " "
                    if match == NOTEXACT:
                        match_string = match_string + "SILVER"+ " "

                self.message_label.setText(match_string)

            self.number_of_attempts.setText(str(self.total_attempts))
            self.total_attempts = self.total_attempts + 1

        except Exception as error:

            self.message_label.setText(str(error))


    def winUI(self):
    
        self.available_colors = []
        self.user_selected_colors = []
        self.updateLists()

        self.message_label.setText("Congratulations You Win !!")
        

    def looseUI(self):

        solution = ""
        for color in self.selected_colors:
            solution = solution + color.name +" "
        self.available_colors = []
        self.user_selected_colors = []
        self.updateLists()

        self.message_label.setText("Sorry You Loose!!\nSolution: " + solution)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = MastermindGame()
    game.show()
    sys.exit(app.exec_())
