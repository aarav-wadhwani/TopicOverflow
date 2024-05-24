import clip
import torch
from PIL import Image
import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Classifier:
    
    def __init__(self, img_path):
        self.img_path = img_path

        # Load CLIP model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

        # Define topics and keywords
        self.topics_keywords = {
            "Vectors": ["vector", "magnitude", "direction", "dot product", "cross product"],
            "3D Shapes": ["shape", "cube", "sphere", "cylinder", "3D"],
            "Lines and Planes": ["line", "plane", "slope", "intersection", "parallel"],
            "Vector Calculus": ["gradient", "divergence", "curvature", "integral", "derivative"]
        }
        
        # Extract topic names and tokenize them
        self.topics = list(self.topics_keywords.keys())
        self.text_inputs = torch.cat([clip.tokenize(topic) for topic in self.topics]).to(self.device)

        # Encode text prompts
        with torch.no_grad():
            self.text_features = self.model.encode_text(self.text_inputs)
            self.text_features /= self.text_features.norm(dim=-1, keepdim=True)
    
    def preprocess_image(self):
        image = self.preprocess(Image.open(self.img_path)).unsqueeze(0).to(self.device)
        return image

    def extract_image_embedding(self, image):
        with torch.no_grad():
            self.image_features = self.model.encode_image(image)
            self.image_features /= self.image_features.norm(dim=-1, keepdim=True)
        return self.image_features

    def extract_text_from_image(self):
        return pytesseract.image_to_string(Image.open(self.img_path))

    def check_keywords(self, text, topic):
        keywords = self.topics_keywords[topic]
        for keyword in keywords:
            if keyword.lower() in text.lower():
                return True
        return False

    def classify_image(self):
        image = self.preprocess_image()
        image_features = self.extract_image_embedding(image)
        
        # Calculate cosine similarity between image and text embeddings
        cosine_similarities = torch.mm(image_features, self.text_features.T)
        best_match_idx = cosine_similarities.argmax(dim=-1).item()
        
        best_match_topic = self.topics[best_match_idx]
        
        # Extract text from image and check for keywords
        extracted_text = self.extract_text_from_image()
        if self.check_keywords(extracted_text, best_match_topic):
            return best_match_topic
        else:
            # Optionally, you can check for other topics if the best match doesn't contain keywords
            for topic in self.topics:
                if self.check_keywords(extracted_text, topic):
                    return topic
            # Default to the best match if no keywords are found
            return best_match_topic



