from PIL import Image
import time

start_time = time.time()

def extract_region(input_image_path, bbox, output_image_path):
    # Open the image
    img = Image.open(input_image_path)
    
    # Crop the image to the specified bounding box
    cropped_img = img.crop(bbox)
    
    # Save the cropped image
    cropped_img.save(output_image_path)

def row_has_only_white_pixels(image_path, row_index):
    # Open the image
    img = Image.open(image_path)
    
    # Get the pixels of the specified row
    pixels = img.load()
    width, height = img.size
    
    # Check if all pixels in the row are white
    for x in range(width):
        pixel = pixels[x, row_index]
        if pixel != (255, 255, 255):  # White pixel represented as (255, 255, 255) in RGB
            return False
    return True

# Example usage
input_image_path = "page-1.png"
img = Image.open(input_image_path)
    
# Get the dimensions
width, height = img.size

section = 1
row = 1
#for each row

while (row < height):
    if (not row_has_only_white_pixels(input_image_path, row)):
        start = row #for start of picture
        row = row + 42 #one row of text has height of 42 pixels
        white_count = 0
        while (True):
            row += 1 #no. of blank rows between lines: 29
            
            while(not row_has_only_white_pixels(input_image_path, row)):
                row = row + 1
                white_count = 0
            
            white_count += 1
            if (white_count >= 120):
                break
                
        bbox = (0, start, width, row-120)  # Example bounding box coordinates (left, upper, right, lower)
        output_image_path = f"section-{section}.png"
        extract_region(input_image_path, bbox, output_image_path)
        section += 1
        row += 20
        
        
    row += 1

print("Process finished --- %s seconds ---" % (time.time() - start_time))