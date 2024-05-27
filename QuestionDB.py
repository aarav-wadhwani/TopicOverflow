import sqlite3
import mysql.connector
import time

from ExtractClass import Extract
from Classify import Classifier

start_time = time.time()

class DBManager:
    
    def __init__(self):
        self.db_name = 'questions'
        self.host = 'localhost'
        self.user = 'Aarav'
        self.password = 'Aarav@TopicOverflow!'
    
    def create_database(self):
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
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

    def insert_question(self, course, professor, year, image_path):
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )
        cursor = conn.cursor()

        # Insert question into 'questions' table
        insert_query = '''
            INSERT INTO questions (course, professor, year, image_path, topic)
            VALUES (%s, %s, %s, %s, %s)
        '''

        classifier = Classifier(image_path)

        insert_data = (course, professor, year, image_path, classifier.classify_image())
        cursor.execute(insert_query, insert_data)

        # Commit changes and close connection
        conn.commit()
        cursor.close()
        conn.close()

    def load_questions(self, db_name='questions.db'):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT course, professor, year, image_path, topic FROM questions')
        question_rows = cursor.fetchall()
        conn.close()
        
        return question_rows
    
    def extract_questions_from_pdf(self, pdf_path):
        extracter = Extract(pdf_path)
        return extracter.extract()

    def process_pdf(self, pdf_path):
        questions = self.extract_questions_from_pdf(pdf_path)
        for course, professor, year, image_path in questions:
            self.insert_question(course, professor, year, image_path)

# Set up the database
# create_database()

# Process a PDF and store questions
#process_pdf('sp19m126e1.pdf')


# Load and display stored questions
# loaded_questions = load_questions()
# for question in loaded_questions:
#     question.display_info()


print("Process finished --- %s seconds ---" % (time.time() - start_time))