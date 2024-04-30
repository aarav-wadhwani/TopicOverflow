from PIL import Image

def extract_region(input_image_path, bbox, output_image_path):
    """
    Extracts a specific region from an image defined by the bounding box (left, upper, right, lower).
    
    Args:
        input_image_path (str): Path to the input image file.
        bbox (tuple): Bounding box coordinates (left, upper, right, lower) of the region to extract.
        output_image_path (str): Path to save the extracted region.
    """
    # Open the image
    img = Image.open(input_image_path)
    
    # Crop the image to the specified bounding box
    cropped_img = img.crop(bbox)
    
    # Save the cropped image
    cropped_img.save(output_image_path)

# Example usage
input_image_path = "page-0.png"
img = Image.open(input_image_path)
    
# Get the dimensions
width, height = img.size

bbox = (0, 0, width, 500)  # Example bounding box coordinates (left, upper, right, lower)
output_image_path = "output_image.png"

extract_region(input_image_path, bbox, output_image_path)
