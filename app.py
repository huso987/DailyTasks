import sys
import pyodbc
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QListWidget, QLabel, QLineEdit, QDateEdit, QComboBox, QListWidgetItem)
from PyQt5.QtGui import QColor, QIcon, QPixmap, QFont
from PyQt5.QtCore import QDate

# SQL Server bağlantı bilgileri
SQL_SERVER = "server yolunu belirtin"
DATABASE = "databaseadı"
TABLE_NAME = "tasks"

# Öncelik renkleri
priority_colors = {
    5: QColor("red"),
    4: QColor("orange"),
    3: QColor("yellow"),
    2: QColor("lightgreen"),
    1: QColor("green")
}


def get_db_connection():
    return pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={SQL_SERVER};'
        f'DATABASE={DATABASE};'
        'Trusted_Connection=yes;'
    )


def get_tasks(date=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if date:
        cursor.execute(f"""
            SELECT id, task, due_date, priority, completed FROM {TABLE_NAME} 
            WHERE due_date = ? ORDER BY due_date ASC, priority DESC
        """, (date,))
    else:
        cursor.execute(f"""
            SELECT id, task, due_date, priority, completed FROM {TABLE_NAME} 
            ORDER BY due_date ASC, priority DESC
        """)
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def add_task(task_name, due_date, priority):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO {TABLE_NAME} (task, due_date, priority, completed) 
        VALUES (?, ?, ?, 0)
    """, (task_name, due_date, priority))
    conn.commit()
    conn.close()


def mark_task_completed(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        UPDATE {TABLE_NAME} SET completed = 1 WHERE id = ?
    """, (task_id,))
    conn.commit()
    conn.close()


class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_tasks()

    def initUI(self):
        self.setWindowTitle("Günlük Yapılacaklar Listesi")
        self.setGeometry(100, 100, 500, 600)
        layout = QVBoxLayout()

        self.task_list = QListWidget()
        self.task_list.itemDoubleClicked.connect(self.complete_task)
        layout.addWidget(QLabel("Yapılacak Görevler:"))
        layout.addWidget(self.task_list)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Görev adını giriniz")
        layout.addWidget(self.task_input)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        self.priority_input = QComboBox()
        self.priority_input.addItems(["1", "2", "3", "4", "5"])
        layout.addWidget(self.priority_input)

        self.add_btn = QPushButton("Görev Ekle")
        self.add_btn.clicked.connect(self.add_task)
        layout.addWidget(self.add_btn)

        self.today_btn = QPushButton("Bugünkü Görevleri Getir")
        self.today_btn.clicked.connect(self.load_today_tasks)
        layout.addWidget(self.today_btn)

        self.all_tasks_btn = QPushButton("Tüm Görevleri Getir")
        self.all_tasks_btn.clicked.connect(self.load_tasks)
        layout.addWidget(self.all_tasks_btn)

        self.setLayout(layout)

    def load_tasks(self, date=None):
        self.task_list.clear()
        tasks = get_tasks(date)
        last_date = None

        for task in tasks:
            task_id, task_name, due_date, priority, completed = task

            if last_date != due_date:
                separator_item = QListWidgetItem(f"--- {due_date} ---")
                separator_item.setFlags(separator_item.flags() & ~3)
                self.task_list.addItem(separator_item)
                last_date = due_date

            item_text = f"{task_name} (Önem: {priority})"
            if completed:
                item_text += " ✔"

            item = QListWidgetItem(item_text)
            if completed:
                item.setForeground(QColor("gray"))
                font = QFont()
                font.setStrikeOut(True)
                item.setFont(font)

            color = priority_colors.get(priority, QColor("black"))
            pixmap = QPixmap(20, 20)
            pixmap.fill(color)
            icon = QIcon(pixmap)
            item.setIcon(icon)

            item.setData(32, task_id)
            self.task_list.addItem(item)

    def load_today_tasks(self):
        today = QDate.currentDate().toString("yyyy-MM-dd")
        self.load_tasks(today)

    def add_task(self):
        task_name = self.task_input.text()
        due_date = self.date_input.date().toString("yyyy-MM-dd")
        priority = int(self.priority_input.currentText())
        if task_name:
            add_task(task_name, due_date, priority)
            self.task_input.clear()
            self.load_tasks()

    def complete_task(self, item):
        task_id = item.data(32)
        mark_task_completed(task_id)
        self.load_tasks()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())
