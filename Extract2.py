from pypdf import PdfReader as reader
from PIL import Image
import fitz  # PyMuPDF
import time
import os

start_time = time.time()
global q
q = 1

def get_text_coordinates(pdf_path, search_text):

    text_coordinates = []
    
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        
        # Search for the text on the page
        for text_instance in page.search_for(search_text):
            # Extract the coordinates of the text instance
            x0, y0, x1, y1 = text_instance
            text_coordinates.append({
                'page': page_num + 1,  # Page number (1-based index)
                'x0': x0,
                'y0': y0,
                'x1': x1,
                'y1': y1,
            })
    
    return text_coordinates

def take_screenshot(pdf_path, pg_no, start_row, end_row):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    i = 1
    for page in pdf_document:
        if(i == pg_no):
            image = page.get_pixmap(matrix=fitz.Matrix(4, 4))  # You can adjust the scaling factor if needed
            image.save(f"page-{i}.png")
            img = Image.open(f"page-{i}.png")
            width, height = img.size
            crop_section = (0, start_row, width, end_row)
            cropped_image = img.crop(crop_section)
            global q
            cropped_image.save(f"question-{q}.png")
            os.remove(f"page-{i}.png")
            q += 1
        i += 1


pdf_path = "sp19m126e1.pdf"  # Replace with the path to your PDF file
for ch in "abc":
    search_text = f"({ch})"  # Text to search for in the PDF
    text_coordinates = get_text_coordinates(pdf_path, search_text)

    for coord in text_coordinates:
        print("Page {}, Question {}, Coordinates: ({}, {}) - ({}, {})".format(coord['page'], search_text, coord['x0'], coord['y0'], coord['x1'], coord['y1']))
        start = coord['y0']+175 #as per tests
        row = start
        #Currently hard coded based on paterns of sp19m126e1.pdf, needs to be changed
        if(search_text == "(a)"):
            take_screenshot(pdf_path, coord['page'], start-150, row+380)
        elif(search_text == "(b)"):
            take_screenshot(pdf_path, coord['page'], start+500, row+950)
        else:
            take_screenshot(pdf_path, coord['page'], start+1000, row+1450)


print("Process finished --- %s seconds ---" % (time.time() - start_time))