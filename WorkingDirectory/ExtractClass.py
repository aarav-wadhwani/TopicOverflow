from pypdf import PdfReader as reader
from PIL import Image
import fitz  # PyMuPDF
import os

from ExtractData import PdfData

class Extract:
    
    global q
    q = 1

    def __init__(self, pdf_path, quesions=[]):
        self.pdf_path = pdf_path
        self.questions = quesions

    def get_text_coordinates(self, search_text):

        text_coordinates = []
        
        # Open the PDF file
        pdf_document = fitz.open(self.pdf_path)
        
        # Iterate through each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # Search for the text on the page
            for text_instance in page.search_for(search_text):
                # Extract the coordinates of the text instance
                x0, y0, x1, y1 = text_instance
                text_coordinates.append({
                    'page': page_num + 1,  # Page number (1-based index)
                    'y0': y0,
                })
        
        return text_coordinates

    def get_end_text_coordinates(self, page_num, search_text):
        
        # Open the PDF file
        pdf_document = fitz.open(self.pdf_path)
        page = pdf_document.load_page(page_num)
        
        text_coordinates = []

        # Search for the text on the page
        for text_instance in page.search_for(search_text):
            # Extract the coordinates of the text instance
            x0, y0, x1, y1 = text_instance
            text_coordinates.append(y0)
        
        return text_coordinates

    def take_screenshot(self, pg_no, start_row, end_row, isEnd):
        # Open the PDF file
        pdf_document = fitz.open(self.pdf_path)
        
        i = 1
        
        for page in pdf_document:
            
            if(i == pg_no):
            
                # creating image of page
                image = page.get_pixmap(matrix=fitz.Matrix(4, 4))
                image.save(f"page-{i}.png")
                img = Image.open(f"page-{i}.png")
                width, height = img.size
                
                # pdf text coordinate system
                x0, y0, x1, y1 = page.rect
                page_height = y1-y0
                
                # checking for edge case of last question
                if(isEnd):
                    end_row = page_height
                
                # scaling text coordinates to pixel coordinates
                start_row = start_row * (height/page_height)
                end_row = end_row * (height/page_height)

                # cropping and saving
                crop_section = (0, start_row, width, end_row)
                cropped_image = img.crop(crop_section)
                global q
                cropped_image.save(f"{self.pdf_path}-question-{q}.png")

                # adding to list of questions to add to db
                pd = PdfData(self.pdf_path)
                self.questions.append((pd.getCourse(), pd.getProf(), pd.getDate(), f"{self.pdf_path}-question-{q}.png"))
                os.remove(f"page-{i}.png")
                q += 1
                
            i += 1

    def extract(self):

        for ch in "abc":
            
            search_text_start = f"({ch})"  # Text to search for in the PDF
            text_coordinates_start = self.get_text_coordinates(search_text_start)

            count = 0
            for coord1 in text_coordinates_start:
                
                print("Page {}, Question {}, Coordinates: ({}))".format(coord1['page'], search_text_start, coord1['y0']))
                start = coord1['y0']
                end = None
                count2 = 0
                for coord2 in  self.get_end_text_coordinates(coord1['page']-1, f"({chr(ord(ch) + 1)})"):
                    if(count == count2): 
                        end = coord2
                        break
                    count2 += 1

                if(not end is None): 
                    self.take_screenshot(coord1['page'], start-5, end, False)
                else:
                    self.take_screenshot(coord1['page'], start-5, 0, True)

                count+=1
        
        return self.questions
