from QuestionDB import DBManager
import inquirer
from datetime import datetime
from PIL import Image
from fpdf import FPDF
import os
import string

print("Welcome to TopicOverflow!")
print("Please provide the following information:")

courses = ["Math 124", "Math 125", "Math 126"]
professors = ["Dr. Loveless", "Dr. Ostroff", "Dr. Camacho"]
current_year = datetime.now().year
years = [str(year) for year in range(current_year - 14, current_year + 1)]
topics = ["Vectors", "3D Shapes", "Lines and Planes", "Vector Calculus"]

questions = [
    inquirer.List('course',
                    message="Select your course",
                    choices=courses),
    inquirer.List('professor',
                    message="Select your professor",
                    choices=professors),
    inquirer.Checkbox('years',
                        message="Select the years",
                        choices=years),
    inquirer.List('topic',
                    message="Select the topic",
                    choices=topics),
]

answers = inquirer.prompt(questions)

print("\nThank you for providing the details. Here is the information you selected:")
print(f"Course: {answers['course']}")
print(f"Professor: {answers['professor']}")
print(f"Years: {', '.join(answers['years'])}")
print(f"Topic: {answers['topic']}")

dbm = DBManager('Aarav', 'Aarav@TopicOverflow!')

questions = dbm.load_questions()

selectedQuestions = []

answers['years'] = list(answers['years'])

for question in questions:
    if(question[4] == answers['topic'] and str(question[2]) in answers['years'] and question[3] not in selectedQuestions):
        selectedQuestions.append(question[3])
        answers['years'].remove(str(question[2]))
    
for q in selectedQuestions:
    print(q)

pdf_path = "output.pdf"

images = [
    Image.open(f)
    for f in selectedQuestions
]

images[0].save(
    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
)
print("PDF created successfully: " + pdf_path)