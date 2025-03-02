# DailyTasks
A simple To-Do list application built with PyQt5 and SQL Server. Users can add tasks, view them, and mark them as completed with priority levels indicated by color coding.

## Features

- Add, view, and mark tasks as completed
- Store tasks in a SQL Server database
- Prioritize tasks with color coding (Red for high priority, green for low)
- Tasks are displayed based on due date, and can be filtered by today's tasks or all tasks

## Main Application Window
![image](https://github.com/user-attachments/assets/912dd7d6-3caf-4195-b479-475da7d87a73)

## Requirements

- Python 3.x
- pyodbc
- PyQt5
- SQL Server

## Installation

### 1. Clone the repository

Clone the repository to your local machine:

git clone https://github.com/huso987/DailyTasks.git
cd DailyTasks

### 2. Install required packages

Install the required dependencies using pip: 
pip install -r requirements.txt

### 3. Configure your database
Make sure you have a SQL Server instance running with a database. The application expects a table named tasks in your database with the following structure:
CREATE TABLE tasks (
    id INT PRIMARY KEY IDENTITY,
    task NVARCHAR(255),
    due_date DATE,
    priority INT,
    completed BIT
);

You need to update the connection string in app.py with your own SQL Server details:
SQL_SERVER = r"your_sql_server"
DATABASE = "your_database"

### 4.Run the application 
Once the database is configured, you can start the application:
python app.py

## Usage
Add a task: Enter the task name, select a due date, and choose a priority level (1-5).
Mark a task as completed: Double-click a task to mark it as completed. Completed tasks will be displayed with a strike-through and in gray color.
View tasks: You can view all tasks or filter tasks to show only today's tasks.

## Steps to Create the Executable

1. **Install PyInstaller**

   If you don't have PyInstaller installed, you can install it via pip:
   pip install pyinstaller
   
2. **Navigate to Your Project Directory**

   Open a terminal or command prompt and navigate to the directory where your app.py file is located.

3. **Run PyInstaller Command**

   To create a single executable file without a console window and with a custom icon, run the following command:

   pyinstaller --onefile --noconsole --icon=icon.ico app.py


