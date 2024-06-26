'''This is the main program to be ran after ExtractClass and Organizer, respectively, have been ran'''

import inquirer
import mysql.connector
from mysql.connector import Error

# Function to connect to the MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='Hemil',  # Replace with your MySQL username
            password='Hemil@TopicOverflow!',  # Replace with your MySQL password
            database='questions_db'  # Replace with your database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Function to execute SQL queries and retrieve data based on user input
def query_database(connection, professor, exam_type, term, topic):
    try:
        cursor = connection.cursor()
        query = '''
            SELECT id, professor FROM image_metadata
            WHERE professor = %s
            AND exam_type = %s
            AND term = %s
            AND topic = %s
        '''
        print("Executing query:", query % (professor, exam_type, term, topic))  # For debugging
        cursor.execute(query, (professor, exam_type, term, topic))
        data = cursor.fetchall()
        cursor.close()
        return data
    except Error as e:
        print(f"Error querying database: {e}")
        return None



# Function to prompt user for input using inquirer
def prompt_user():
    # List of options for user selection
    professors = ["Dr.Loveless", "Dr.Bekyel", "Dr.Camacho"]
    exam_types = ["mid1", "mid2", "final"]
    terms = ["sp23", "wi24"]
    topics = ["Limits", "3D Shapes", "Lines and Planes", "Vector Calculus"]

    # Questions for user input
    questions = [
        inquirer.List('professor',
                      message="Select your professor",
                      choices=professors),
        inquirer.List('exam_type',
                      message="Select the exam type",
                      choices=exam_types),
        inquirer.List('term',
                      message="Select the term",
                      choices=terms),
        inquirer.List('topic',
                      message="Select the topic",
                      choices=topics),
    ]

    # Prompt user for inputs
    answers = inquirer.prompt(questions)
    return answers

if __name__ == "__main__":
    # Connect to the MySQL database
    connection = connect_to_database()
    if connection:
        # Prompt user for input
        user_input = prompt_user()

        # Query the database based on user input
        data = query_database(connection, user_input['professor'], user_input['exam_type'], user_input['term'], user_input['topic'])

        if data:
            # Display or process the retrieved data
            for row in data:
                print(row)  # Print each row of data
        else:
            print("No data found")

        # Close the database connection
        connection.close()
