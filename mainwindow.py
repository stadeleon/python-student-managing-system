import sys
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QTableWidgetItem, \
    QDialog, QVBoxLayout, QComboBox
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Managing System")
        self.resize(600, 600)


        file_menu_item = self.menuBar().addMenu("&File")
        add_student_action = QAction("Add student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        help_menu_item = self.menuBar().addMenu("&Help")
        about_action = QAction("Help", self)
        help_menu_item.addAction(about_action)

        edit_menu_item = self.menuBar().addMenu("&Edit")
        find_action = QAction("Search", self)
        find_action.triggered.connect(self.search)
        edit_menu_item.addAction(find_action)

        # about_action.setMenuRole(QAction.MenuRole.NoRole)  ## use this line only if "Help" not displayed

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("Select * from students")

        self.table.setRowCount(0)
        for row_num, row in enumerate(result):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Student Name")

        layout.addWidget(self.search_name)

        button = QPushButton("Search")
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        pass

class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add dropdown list of courses
        self.course_name = QComboBox()
        courses = ['Math', 'Astronomy', 'Biology', 'Physics']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # Add submit button
        button = QPushButton('Add Student')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("Insert into students (name, course, mobile) Values (?, ?, ?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        manager.load_data()


app = QApplication(sys.argv)
manager = MainWindow()
manager.show()
manager.load_data()
sys.exit(app.exec())

