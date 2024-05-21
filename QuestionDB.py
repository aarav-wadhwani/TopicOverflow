import sqlite3
import mysql.connector

from ExtractClass import Extract

class Question:
    def __init__(self, course, professor, year, image_path, topic=None):
        self.course = course
        self.professor = professor
        self.year = year
        self.image_path = image_path
        self._topic = topic

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, value):
        self._topic = value

    def display_info(self):
        print(f"Course: {self.course}")
        print(f"Professor: {self.professor}")
        print(f"Year: {self.year}")
        print(f"Image Path: {self.image_path}")
        print(f"Topic: {self.topic}")

    def get_image(self):
        print(f"Loading image from {self.image_path}")

def create_database(db_name='questions', host='localhost', user='Aarav', password='Aarav@TopicOverflow!'):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = conn.cursor()

    # Create 'questions' table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            course VARCHAR(255),
            professor VARCHAR(255),
            year INT,
            image_path VARCHAR(255),
            topic VARCHAR(255)
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()

def insert_question(course, professor, year, image_path, topic, db_name='questions', host='localhost', user='Aarav', password='Aarav@TopicOverflow!'):
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = conn.cursor()

    # Insert question into 'questions' table
    insert_query = '''
        INSERT INTO questions (course, professor, year, image_path, topic)
        VALUES (%s, %s, %s, %s, %s)
    '''
    insert_data = (course, professor, year, image_path, topic)
    cursor.execute(insert_query, insert_data)

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()

def load_questions(db_name='questions.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT course, professor, year, image_path, topic FROM questions')
    question_rows = cursor.fetchall()
    conn.close()
    
    questions = [Question(row[0], row[1], row[2], row[3], row[4]) for row in question_rows]
    return questions

def extract_questions_from_pdf(pdf_path):
    extracter = Extract(pdf_path)
    return extracter.extract()

def process_pdf(pdf_path):
    questions = extract_questions_from_pdf(pdf_path)
    for course, professor, year, image_path, topic in questions:
        insert_question(course, professor, year, image_path, topic)

# Set up the database
# create_database()

# Process a PDF and store questions
process_pdf('sp19m126e1.pdf')

# Load and display stored questions
loaded_questions = load_questions()
for question in loaded_questions:
    question.display_info()
