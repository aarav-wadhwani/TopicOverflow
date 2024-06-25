from PIL import Image
import fitz  # PyMuPDF
import os

class Extract:
    
    global q
    q = 1

    def __init__(self, pdf_path, output_folder, questions=[]):
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        self.questions = questions

    def get_text_coordinates(self, search_text):
        text_coordinates = []
        pdf_document = fitz.open(self.pdf_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            for text_instance in page.search_for(search_text):
                x0, y0, x1, y1 = text_instance
                text_coordinates.append({
                    'page': page_num + 1,
                    'y0': y0,
                })
        return text_coordinates

    def get_end_text_coordinates(self, page_num, search_text):
        pdf_document = fitz.open(self.pdf_path)
        page = pdf_document.load_page(page_num)
        text_coordinates = []
        for text_instance in page.search_for(search_text):
            x0, y0, x1, y1 = text_instance
            text_coordinates.append(y0)
        return text_coordinates

    def take_screenshot(self, pg_no, start_row, end_row, isEnd):
        pdf_document = fitz.open(self.pdf_path)
        i = 1
        for page in pdf_document:
            if i == pg_no:
                image = page.get_pixmap(matrix=fitz.Matrix(4, 4))
                image.save(f"page-{i}.png")
                img = Image.open(f"page-{i}.png")
                width, height = img.size
                x0, y0, x1, y1 = page.rect
                page_height = y1 - y0
                if isEnd:
                    end_row = page_height
                start_row = start_row * (height / page_height)
                end_row = end_row * (height / page_height)
                crop_section = (0, start_row, width, end_row)
                cropped_image = img.crop(crop_section)
                global q
                output_path = os.path.join(self.output_folder, f"{os.path.basename(self.pdf_path)}-question-{q}.png")
                cropped_image.save(output_path)
                self.questions.append(output_path)
                os.remove(f"page-{i}.png")
                q += 1
            i += 1

    def extract(self):
        for ch in "abc":
            search_text_start = f"({ch})"
            text_coordinates_start = self.get_text_coordinates(search_text_start)
            count = 0
            for coord1 in text_coordinates_start:
                print("Page {}, Question {}, Coordinates: ({}))".format(coord1['page'], search_text_start, coord1['y0']))
                start = coord1['y0']
                end = None
                count2 = 0
                for coord2 in self.get_end_text_coordinates(coord1['page'] - 1, f"({chr(ord(ch) + 1)})"):
                    if count == count2: 
                        end = coord2
                        break
                    count2 += 1
                if end is not None:
                    self.take_screenshot(coord1['page'], start - 5, end, False)
                else:
                    self.take_screenshot(coord1['page'], start - 5, 0, True)
                count += 1
        return self.questions

def process_pdfs_in_folder(folder_path, output_folder):
    all_questions = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            extractor = Extract(pdf_path, output_folder)
            questions = extractor.extract()
            all_questions.extend(questions)
    return all_questions

if __name__ == "__main__":
    folder_path = r'C:\Users\Hemil Patel\Desktop\TOv0\m126'
    output_folder = r'C:\Users\Hemil Patel\Desktop\TOv0\m126\Images'
    all_extracted_questions = process_pdfs_in_folder(folder_path, output_folder)
    for question in all_extracted_questions:
        print(question)