from pypdf import PdfReader as reader

class PdfData:
  
  def __init__(self, pdf_path):
    self.pdf_path = pdf_path
    self.setup()

  def setup(self):
    
    r = reader(self.pdf_path)

    # creating a page object
    page = r.pages[0]

    # creating an array of lines
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

    # extracting only course details (not quarter and year)
    course = ""
    prev_char = ''
    for char in textLines[0]:
      if(char == ' ' and prev_char.isdigit()):
        break
      else:
        course = course + char
        prev_char = char
    
    self.prof = "Dr. Loveless"
    self.year = textLines[2][-4:]
    self.course = course
    self.picture = ''
  
  def getDate(self):
     return self.year
  
  def getProf(self):
     return self.prof
  
  def getCourse(self):
     return self.course


#Finding the quarter from the month
# month = ""
# for c in textLines[2]:
#   if(c == ' '):
#     break
#   month = month + c
# quarter = ""
# if(month == "April" or month == "May" or month == "June"):
#   quarter = "Spring"
# elif(month == "July" or month == "August" or month == "September"):
#   quarter = "Summer"
# elif(month == "October" or month == "November" or month == "December"):
#   quarter = "Fall"
# else:
#   quarter = "Winter"

#sample object of class object
#q1 = PdfData("Dr. Loveless", textLines[2], course, quarter)
#print(q1)
