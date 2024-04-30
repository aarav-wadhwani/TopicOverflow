from pypdf import PdfReader as reader

class Question:
  def __init__(self, prof, date, course, quarter):
    self.prof = prof
    self.date = date
    self.course = course
    self.quarter = quarter
    self.picture = ''

  def __str__(self):
      return f"This is a {self.course} paper made by {self.prof} on {self.date} for the {quarter} quarter"

r = reader('sp19m126e1.pdf')

# creating a page object
page = r.pages[0]

#creating an array of lines
textLines = []
i = 0
line = ""
for c in page.extract_text():
    if(c == '\n'):
        i = 0
        textLines.append(line)
        line = ""
    else:
        line = line + c
    i = i+1

#extracting only course details (not quarter and year)
course = ""
prev_char = ''
for char in textLines[0]:
  if(char == ' ' and prev_char.isdigit()):
    break
  else:
    course = course + char
    prev_char = char

#Finding the quarter from the month
month = ""
for c in textLines[2]:
  if(c == ' '):
    break
  month = month + c
quarter = ""
if(month == "April" or month == "May" or month == "June"):
  quarter = "Spring"
elif(month == "July" or month == "August" or month == "September"):
  quarter = "Summer"
elif(month == "October" or month == "November" or month == "December"):
  quarter = "Fall"
else:
  quarter = "Winter"

#sample object of class object
q1 = Question("Dr. Loveless", textLines[2], course, quarter)
print(q1)
