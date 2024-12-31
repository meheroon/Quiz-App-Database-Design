import sqlite3
from datetime import datetime

# Establishing SQLite Connection
def create_connection():
    connection = sqlite3.connect("quiz_app.db")
    return connection

# Create tables as per the schema
def create_tables():
    conn = create_connection()
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT CHECK(role IN ('student', 'teacher')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    # Quizzes table
    c.execute('''CREATE TABLE IF NOT EXISTS Quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        teacher_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES Users (id)
    )''')

    # Questions table
    c.execute('''CREATE TABLE IF NOT EXISTS Questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        text TEXT NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES Quizzes (id)
    )''')

    # Options table
    c.execute('''CREATE TABLE IF NOT EXISTS Options (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_id INTEGER,
        text TEXT NOT NULL,
        is_correct BOOLEAN,
        FOREIGN KEY (question_id) REFERENCES Questions (id)
    )''')

    # Student Answers table
    c.execute('''CREATE TABLE IF NOT EXISTS Student_Answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        quiz_id INTEGER,
        question_id INTEGER,
        option_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES Users (id),
        FOREIGN KEY (quiz_id) REFERENCES Quizzes (id),
        FOREIGN KEY (question_id) REFERENCES Questions (id),
        FOREIGN KEY (option_id) REFERENCES Options (id)
    )''')

    conn.commit()
    conn.close()

# Function to add a user
def add_user(name, role):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO Users (name, role) VALUES (?, ?)", (name, role))
    conn.commit()
    conn.close()

# Function to add a quiz
def add_quiz(title, teacher_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO Quizzes (title, teacher_id) VALUES (?, ?)", (title, teacher_id))
    conn.commit()
    conn.close()

# Function to add a question to a quiz
def add_question(quiz_id, text):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO Questions (quiz_id, text) VALUES (?, ?)", (quiz_id, text))
    conn.commit()
    conn.close()

# Function to add an option to a question
def add_option(question_id, text, is_correct):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO Options (question_id, text, is_correct) VALUES (?, ?, ?)", (question_id, text, is_correct))
    conn.commit()
    conn.close()

# Function to add a student's answer
def add_student_answer(student_id, quiz_id, question_id, option_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO Student_Answers (student_id, quiz_id, question_id, option_id) VALUES (?, ?, ?, ?)",
              (student_id, quiz_id, question_id, option_id))
    conn.commit()
    conn.close()

# Sample operations
def initialize_sample_data():
    # Adding a teacher
    add_user("John Doe", "teacher")
    teacher_id = 1
    
    # Creating a quiz by the teacher
    add_quiz("Math Quiz", teacher_id)
    quiz_id = 1
    
    # Adding questions to the quiz
    add_question(quiz_id, "What is 2 + 2?")
    question_id = 1
    # Adding options for the question
    add_option(question_id, "4", True)
    add_option(question_id, "5", False)
    
    # Adding a student
    add_user("Student A", "student")
    student_id = 2
    
    # Recording a student's answer
    add_student_answer(student_id, quiz_id, question_id, 1)  # Option 1 is correct (4)

# Initialize tables and sample data
create_tables()
initialize_sample_data()

