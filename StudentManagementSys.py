import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QStatusBar
)

# Student data file name
STUDENTS_FILE = "students.json"    

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
        self.setGeometry(100, 100, 600, 400)

        # Main widget initialization
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Welcome to the Student Management System", 5000)

        # Input area
        self.input_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.grade_input = QLineEdit()
        self.dni_input = QLineEdit()

        self.input_layout.addWidget(QLabel("Name:"))
        self.input_layout.addWidget(self.name_input)
        self.input_layout.addWidget(QLabel("Age:"))
        self.input_layout.addWidget(self.age_input)
        self.input_layout.addWidget(QLabel("Grade:"))
        self.input_layout.addWidget(self.grade_input)
        self.input_layout.addWidget(QLabel("DNI:"))
        self.input_layout.addWidget(self.dni_input)

        # Button area
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Student")
        self.delete_button = QPushButton("Delete Student")
        self.update_button = QPushButton("Update Student")

        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.update_button)

        # Student list
        self.student_list = QListWidget()

        # Add widgets to the main layout
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.student_list)

        # Connect the buttons to the functions
        self.add_button.clicked.connect(self.add_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.update_button.clicked.connect(self.update_student)
        self.student_list.itemSelectionChanged.connect(self.select_student)

        # Update student list
        self.update_student_list()
        
    def update_student_list(self):
        self.student_list.clear()
        students = load_students()
        for student in students:
            self.student_list.addItem(
                f"{student['name']} - {student['age']} years old - Grade {student['grade']} - DNI: {student['dni']}"
            )

    def add_student(self):
        name = self.name_input.text().strip()
        age = self.age_input.text().strip()
        grade = self.grade_input.text().strip()
        dni = self.dni_input.text().strip()
        student = {"name": name, "age": age, "grade": grade, "dni": dni}
        if name and age and grade and dni:
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
        selected = self.student_list.currentRow()      # Get the selected student, if theres any, if not, return -1
        if selected >= 0:
            students = load_students()
            del students[selected]                     # Delete the student from the list with corresponding index
            save_students(students)
            self.update_student_list()
            self.student_list.clearSelection()
            self.clear_inputs()
            self.status_bar.showMessage("Student deleted successfully!", 5000)
        else:
            QMessageBox.warning(self, "Error", "Please select a student to delete!")

    def update_student(self):
        selected = self.student_list.currentRow()
        if selected >= 0:
            name = self.name_input.text().strip()
            age = self.age_input.text().strip()
            grade = self.grade_input.text().strip()
            dni = self.dni_input.text().strip()
            student = {"name": name, "age": age, "grade": grade, "dni": dni}
            if name and age and grade and dni:
                if not self.check_OK(student):
                    return
                if self.dni_exists(dni):
                    QMessageBox.warning(self, "Error", "DNI already exists!")
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

    def select_student(self):
        selected = self.student_list.currentRow() 
        if selected >= 0:
            students = load_students()
            if selected < len(students):  
                student = students[selected]
                self.name_input.setText(student["name"])
                self.age_input.setText(student["age"])
                self.grade_input.setText(student["grade"])
                self.dni_input.setText(student["dni"])

    def dni_exists(self,dni):
        students = load_students()
        for student in students:
            if student['dni'] == dni:
                return True
        return False
    
    def check_OK(self,student):
        if not student['age'].isdigit():
            QMessageBox.warning(self, "Error", "Age must be a number!")
            return
        if not student['grade'].isdigit():
            QMessageBox.warning(self, "Error", "Grade must be a number!")
            return
        if len(student['dni']) != 8 or not student['dni'].isdigit():
            QMessageBox.warning(self, "Error", "DNI must be an 8-digit number!")
            return

    def clear_inputs(self):
        self.name_input.clear()
        self.age_input.clear()
        self.grade_input.clear()
        self.dni_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)        # Create the application, sys.argv passes the command line arguments to the application
    window = StudentManagementApp()     # Create the main window
    window.show()                       # Show the main window
    sys.exit(app.exec_())               # Start the application event loop