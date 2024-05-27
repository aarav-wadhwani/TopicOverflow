from QuestionDB import DBManager

dbm = DBManager('Aarav', 'Aarav@TopicOverflow!')

questions = dbm.load_questions()

selectedQuestions = []
i = 0
for question in questions:
    if(question[4] == 'Lines and Planes'):
        selectedQuestions.append(question[3])
    
for q in selectedQuestions:
    print(q)