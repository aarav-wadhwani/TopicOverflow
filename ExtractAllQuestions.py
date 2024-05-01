from PIL import Image

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
input_image_path = "page-0.png"
img = Image.open(input_image_path)
    
# Get the dimensions
width, height = img.size

#for each row
for row in range(height):
    if(not row_has_only_white_pixels(input_image_path, row)):
        start = row
        row = row + 42 #one row of text has height of 42 pixels
        while (row_has_only_white_pixels(input_image_path, row)):
            row = row + 29 #no. of blank rows between lines: 29
            if(not row_has_only_white_pixels(input_image_path, row)):
                row = row + 42
        bbox = (0, start - 20, width, row+20)  # Example bounding box coordinates (left, upper, right, lower)
        output_image_path = "output_image.png"
        extract_region(input_image_path, bbox, output_image_path)
        break
