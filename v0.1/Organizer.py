"""
This script is designed to process PNG images extracted from PDF files, classify their topics using OCR with Tesseract,
add relevant metadata to the images, and store this metadata in a MySQL database. The main functionalities include:

Metadata is defined as data of data. In this case, the original data (the image) needs to have its own data which is the course, the topic, the professor, 
exam type, and the term.

1. Extracting metadata such as professor, exam type, and term from the image filenames.
2. Classifying the topic of the image content using Tesseract OCR and keyword matching.
    2.1 I have willing removed the ML model since I am now training our own ML model.
    We should have never used CLIP, it is not made for out application.
3. Adding extracted metadata and classified topic as metadata to the images.
4. Connecting to a MySQL database to store the image metadata.
5. Creating a table in the database to store the metadata.
6. Inserting the extracted metadata into the database.
7. Reading and printing the metadata from the images.
"""

from PIL import Image, PngImagePlugin
import os
import pytesseract
import mysql.connector
from mysql.connector import Error

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_metadata_from_filename(filename):
    # Remove the ".png" extension
    filename_without_extension = filename.replace(".png", "")
    # Remove the ".pdf-question-1" suffix if it exists
    filename_without_suffix = filename_without_extension.split(".pdf")[0]
    parts = filename_without_suffix.split("_")
    if len(parts) == 3:
        professor = "Dr." + parts[0].capitalize()
        exam_type = parts[1]
        term = parts[2]
    else:
        professor = "Unknown"
        exam_type = "Unknown"
        term = "Unknown"
    return professor, exam_type, term

# This classifier is really basic, in fact it is not even accurate.
# I wrote it just for it to get along with the whole process of classiification
# while the personalised ML model is being made.
def classify_topic(image_path):
    # Placeholder function for topic classification using keyword matching
    # You can replace this with your actual topic classification logic
    extracted_text = pytesseract.image_to_string(Image.open(image_path))
    # Example keyword matching
    if "lim" in extracted_text.lower():
        return "Limits"
    elif "shape" in extracted_text.lower():
        return "3D Shapes"
    elif "line" in extracted_text.lower():
        return "Lines and Planes"
    elif "calculus" in extracted_text.lower():
        return "Vector Calculus"
    else:
        return "Unknown"

def add_metadata_to_image(image_path, professor, exam_type, term, topic):
    img = Image.open(image_path)
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Professor", professor)
    meta.add_text("Exam Type", exam_type)
    meta.add_text("Term", term)
    meta.add_text("Topic", topic)  # Add the topic metadata
    
    img.save(image_path, "PNG", pnginfo=meta)

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='',  # Replace with your MySQL username
            password='',  # Replace with your MySQL password
            database=''  # Replace with your new database name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_metadata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                professor VARCHAR(255),
                exam_type VARCHAR(255),
                term VARCHAR(255),
                topic VARCHAR(255),
                image_path VARCHAR(255)
            )
        ''')
        connection.commit()
        cursor.close()
        print("Table created successfully")
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, professor, exam_type, term, topic, image_path):
    try:
        cursor = connection.cursor()
        insert_query = '''
            INSERT INTO image_metadata (professor, exam_type, term, topic, image_path)
            VALUES (%s, %s, %s, %s, %s)
        '''
        insert_data = (professor, exam_type, term, topic, image_path)
        cursor.execute(insert_query, insert_data)
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")

def process_images_and_store_data(folder_path, connection):
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            professor, exam_type, term = extract_metadata_from_filename(filename)
            topic = classify_topic(image_path)  # Classify the topic using keyword matching
            add_metadata_to_image(image_path, professor, exam_type, term, topic)
            insert_data(connection, professor, exam_type, term, topic, image_path)

def read_metadata_from_image(image_path):
    img = Image.open(image_path)
    info = img.info
    professor = info.get("Professor", "Not found")
    exam_type = info.get("Exam Type", "Not found")
    term = info.get("Term", "Not found")
    topic = info.get("Topic", "Not found")  # Extract the topic from metadata
    print(f"Image: {image_path}")
    print(f"Professor: {professor}")
    print(f"Exam Type: {exam_type}")
    print(f"Term: {term}")
    print(f"Topic: {topic}")
    print("")

if __name__ == "__main__":
    folder_path = r'replace_with_folder_path_of_where_the_images_are_stored'
    connection = connect_to_database()
    if connection:
        create_table(connection)
        process_images_and_store_data(folder_path, connection)
        connection.close()
