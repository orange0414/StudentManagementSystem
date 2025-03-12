import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QMessageBox, QStatusBar
)
from PyQt5.QtCore import Qt
from datetime import datetime

# Student data file name
NOW = datetime.now()
YEAR = NOW.year
STUDENTS_FILE = "students.json"    
VALID_DNI_LENGTH = [8,9]

# Load data from file and return it
def load_students():
    if not os.path.exists(STUDENTS_FILE):   # Check if the file exists, if not, create it with an empty list
        with open(STUDENTS_FILE, 'w') as f:
            json.dump([], f)
    with open(STUDENTS_FILE, 'r') as f:
        return json.load(f)

# Save data to json file
def save_students(students):
    with open(STUDENTS_FILE, 'w') as f:
        json.dump(students, f, indent=4)

class StudentManagementApp(QMainWindow):
    def __init__(self):
        # Main window initialization
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setGeometry(125, 125, 700, 650)

        # Main widget initialization
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Welcome to the Student Management System", 5000)

        # Input Data area
        self.input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.birthYear_input = QLineEdit()
        self.grade_input = QLineEdit()
        self.dni_input = QLineEdit()

        self.input_layout.addWidget(QLabel("Name:"))
        self.input_layout.addWidget(self.name_input)
        self.input_layout.addWidget(QLabel("Birth year:"))
        self.input_layout.addWidget(self.birthYear_input)
        self.input_layout.addWidget(QLabel("Grade:"))
        self.input_layout.addWidget(self.grade_input)
        self.input_layout.addWidget(QLabel("DNI:"))
        self.input_layout.addWidget(self.dni_input)

        # Basic Button area
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Student")
        self.delete_button = QPushButton("Delete Student")
        self.update_button = QPushButton("Update Student")

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.update_button)

        # Search and Sort layout area
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.sort_button = QPushButton("Sort")
        self.reverse_sort_button = QPushButton("Reverse Sort")
        
        self.search_button.setFixedSize(100,30)
        self.sort_button.setFixedSize(100,30)
        self.reverse_sort_button.setFixedSize(100,30)
        
        self.search_layout.addWidget(QLabel("Search by DNI:"))
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.sort_button)
        self.search_layout.addWidget(self.reverse_sort_button)
        
        # Student table area
        self.student_list = QTreeWidget()
        self.student_list.setColumnCount(4)
        self.student_list.setHeaderLabels(["Name", "Age", "Grade", "DNI"])

        # Add widgets to the main layout
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.search_layout)
        self.layout.addWidget(self.student_list)

        # Connect the buttons to the functions
        self.add_button.clicked.connect(self.add_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.update_button.clicked.connect(self.update_student)
        self.student_list.itemSelectionChanged.connect(self.select_student)
        self.search_button.clicked.connect(self.search_student)
        self.sort_button.clicked.connect(self.sort_students)
        self.reverse_sort_button.clicked.connect(self.reverse_sort_students)

        # Update student list
        self.update_student_list()

    def reverse_sort_students(self):
        if self.student_list.topLevelItemCount() > 0:
            students = load_students()
            students.sort(key=lambda x: x['name'], reverse=True)
            save_students(students)
            self.update_student_list()
            self.status_bar.showMessage("Students sorted by name in reverse order!", 5000)
        else:
            QMessageBox.warning(self, "Error", "No students to sort!")

    def sort_students(self):
        if self.student_list.topLevelItemCount() > 0:
            students = load_students()
            students.sort(key=lambda x: x['name'])
            save_students(students)
            self.update_student_list()
            self.status_bar.showMessage("Students sorted by name!", 5000)
        else:
            QMessageBox.warning(self, "Error", "No students to sort!")

    def select_student(self):
        selected = self.student_list.currentIndex().row()
        students = load_students()
        if 0 <= selected < len(students):
            student = students[selected]
            self.name_input.setText(student['name'])
            self.birthYear_input.setText(student['birthYear'])
            self.grade_input.setText(student['grade'])
            self.dni_input.setText(student['dni'])

    def update_student_list(self):
        self.student_list.clear()
        students = load_students()
        for student in students:
            item = QTreeWidgetItem([student['name'],str(YEAR-int(student['birthYear'])),student['grade'],student['dni']])
            self.student_list.addTopLevelItem(item)
    
    def add_student(self):
        name = self.name_input.text().strip()
        birthYear = self.birthYear_input.text().strip()
        grade = self.grade_input.text().strip()
        dni = self.dni_input.text().strip()
        student = {"name": name, "birthYear": birthYear, "grade": grade, "dni": dni}
        if name and birthYear and grade and dni:
            if not self.check_OK(student):
                return
            if self.dni_exists(dni):
                QMessageBox.warning(self, "Error", "DNI already exists!")
                return
            students = load_students()
            students.append(student)
            save_students(students)
            self.update_student_list()
            self.clear_inputs()
            self.status_bar.showMessage("Student added successfully!", 5000)
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields!")
    
    def delete_student(self):
        selected = self.student_list.currentIndex().row()      # Get the selected student, if theres any, if not, return -1
        if selected >= 0:
            students = load_students()
            del students[selected]                # Delete the student from the list with corresponding index
            save_students(students)
            self.update_student_list()
            self.student_list.clearSelection()
            self.clear_inputs()
            self.status_bar.showMessage("Student deleted successfully!", 5000)
        else:
            QMessageBox.warning(self, "Error", "Please select a student to delete!")

    def update_student(self):
        selected = self.student_list.currentIndex().row()
        if selected >= 0:
            name = self.name_input.text().strip()
            birthYear = self.birthYear_input.text().strip()
            grade = self.grade_input.text().strip()
            dni = self.dni_input.text().strip()
            student = {"name": name, "birthYear": birthYear, "grade": grade, "dni": dni}
            if name and birthYear and grade and dni:
                if not self.check_OK(student):
                    return
                students = load_students()
                students[selected] = student
                save_students(students)
                self.update_student_list()
                self.student_list.clearSelection()
                self.clear_inputs()
                self.status_bar.showMessage("Student updated successfully!", 5000)
            else:
                QMessageBox.warning(self, "Error", "Please fill all fields!")
        else:
            QMessageBox.warning(self, "Error", "Please select a student to update!")

    def search_student(self):
        student_dni = self.search_input.text().strip()
        if self.dni_exists(student_dni):
            students = load_students()
            for student in students:
                if student['dni'] == student_dni:
                    self.name_input.setText(student['name'])
                    self.birthYear_input.setText(student['birthYear'])
                    self.grade_input.setText(student['grade'])
                    self.dni_input.setText(student['dni'])
                    item = self.student_list.findItems(student['dni'], Qt.MatchFlag.MatchExactly,3)
                    self.student_list.scrollToItem(item[0])
                    self.student_list.setCurrentItem(item[0])
        elif student_dni == "":
            QMessageBox.warning(self, "Error", "Please enter a DNI to search!")
        else:
            QMessageBox.warning(self, "Error", "Student not found!")
    
    def dni_exists(self,dni):
        students = load_students()
        for student in students:
            if student['dni'] == dni:
                return True
        return False
    
    def check_OK(self,student):
        if not student["birthYear"].isdigit():
            QMessageBox.warning(self, "Error", "Birth year must be a number!")
            return  False
        elif not int(student['birthYear']) <= NOW.year:
            QMessageBox.warning(self, "Error", "Borth year must be less than current year!")
            return  False
        if not student['grade'].isdigit():
            QMessageBox.warning(self, "Error", "Grade must be a number!")
            return  False
        if not len(student['dni']) in VALID_DNI_LENGTH:
            QMessageBox.warning(self, "Error", "DNI must be an 8~9 digit number!")
            return  False
        return True

    def clear_inputs(self):
        self.name_input.clear()
        self.birthYear_input.clear()
        self.grade_input.clear()
        self.dni_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)        # Create the application, sys.argv passes the command line arguments to the application
    window = StudentManagementApp()     # Create the main window
    window.show()                       # Show the main window
    sys.exit(app.exec_())               # Start the application event loop