import inquirer
from datetime import datetime

def main():
    print("Welcome to TopicOverflow!")
    print("Please provide the following information:")

    courses = ["Math 124", "Math 125", "Math 126"]
    professors = ["Dr. Loveless", "Dr. Ostroff", "Dr. Camacho"]
    current_year = datetime.now().year
    years = [str(year) for year in range(current_year - 10, current_year + 1)]
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

    # Here you can call other functions or methods to process the provided information
    # For example, you can integrate this with the question bank generation functionality

if __name__ == "__main__":
    main()
