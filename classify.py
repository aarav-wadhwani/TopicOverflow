import clip
import torch
from PIL import Image
import pytesseract

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Define topics and keywords
topics_keywords = {
    "Vectors": ["vector", "magnitude", "direction", "dot product", "cross product"],
    "3D Shapes": ["surface", "shape", "cube", "sphere", "cylinder", "3D", "circle"],
    "Lines and Planes": ["line", "plane", "slope", "intersection", "parallel"],
    "Vector Calculus": ["curvature", "integral", "derivative", "polar", "tangent"]
}

# Extract topic names and tokenize them
topics = list(topics_keywords.keys())
text_inputs = torch.cat([clip.tokenize(topic) for topic in topics]).to(device)

# Encode text prompts
with torch.no_grad():
    text_features = model.encode_text(text_inputs)
    text_features /= text_features.norm(dim=-1, keepdim=True)

def preprocess_image(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    return image

def extract_image_embedding(image):
    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
    return image_features

def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

def check_keywords(text, topic):
    keywords = topics_keywords[topic]
    for keyword in keywords:
        if keyword.lower() in text.lower():
            return True
    return False

def classify_image(image_path):
    image = preprocess_image(image_path)
    image_features = extract_image_embedding(image)
    
    # Calculate cosine similarity between image and text embeddings
    cosine_similarities = torch.mm(image_features, text_features.T)
    best_match_idx = cosine_similarities.argmax(dim=-1).item()
    
    best_match_topic = topics[best_match_idx]
    
    # Extract text from image and check for keywords
    extracted_text = extract_text_from_image(image_path)
    if check_keywords(extracted_text, best_match_topic):
        return best_match_topic
    else:
        # Optionally, you can check for other topics if the best match doesn't contain keywords
        for topic in topics:
            if check_keywords(extracted_text, topic):
                return topic
        # Default to the best match if no keywords are found
        return best_match_topic

# Path to the screenshot image
screenshot_image_path = "C:\\Users\\Hemil Patel\\Desktop\\TopicOverflow\\OpenAI CLIP\\clip_exam_classifier\\question-8.png"

# Classify the screenshot image
topic = classify_image(screenshot_image_path)
print(f"Image is classified as: {topic}")
