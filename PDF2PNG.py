import fitz  # PyMuPDF

def take_screenshot(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    i = 0
    for page in pdf_document:
        image = page.get_pixmap(matrix=fitz.Matrix(4, 4))  # You can adjust the scaling factor if needed
        image.save(f"page-{i}.png")
        i = i+1
        if(i == 2):
            break #remove later
    

# Example usage
pdf_path = "sp23m126e1v1.pdf"

take_screenshot(pdf_path)
