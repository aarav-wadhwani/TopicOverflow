from pypdf import PdfReader as reader
from PIL import Image
import fitz  # PyMuPDF
import time
import os

start_time = time.time()

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
            cropped_image.save(f"question-{pg_no-1}.png")
            os.remove(f"page-{i}.png")
        i += 1


pdf_path = "sp23m126e1v1.pdf"  # Replace with the path to your PDF file
for i in range(5):
    search_text = f"{i}. (1"  # Text to search for in the PDF
    text_coordinates = get_text_coordinates(pdf_path, search_text)

    for coord in text_coordinates:
        print("Page {}, Coordinates: ({}, {}) - ({}, {})".format(coord['page'], coord['x0'], coord['y0'], coord['x1'], coord['y1']))
        start = coord['y0']+120 #as per tests
        row = start
        #while(row )
        take_screenshot(pdf_path, coord['page'], start , row+250)


print("Process finished --- %s seconds ---" % (time.time() - start_time))