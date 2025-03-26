# Student Management System

Student Management System

## Description

*Student Management System* is an application developed in Python using **PyQt5**. It allows you to easily manage student records by adding, updating, deleting, and viewing information, which is stored locally in a `students.json` file.

## Features

- **Add Students:**  
  Register students with the following fields:  
  - Name  
  - Year of Birth  
  - Grade  
  - DNI (Identification Number)
  
- **Update Information:**  
  Allows you to modify the data of an existing student.
  
- **Delete Records:**  
  Easily remove a student record.
  
- **View Student List:**  
  Displays a list of all registered students.
  
- **Search by DNI:**  
  Helps you locate students using their DNI.
  
- **Sorting:**  
  Sorts the student list alphabetically (ascending or descending).
  
- **User Feedback:**  
  - The status bar displays success messages.
  - Errors are reported using pop-up windows (`QMessageBox`).

## Requirements

- Python 3.x
- PyQt5

> **Installing PyQt5:**  
> Run the following command in your terminal:
> ```bash
> pip install pyqt5
> ```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <REPOSITORY_URL>
