# model_handler.py
import torch
import numpy as np
from transformers import CLIPProcessor, CLIPModel

class ModelHandler:
    def __init__(self, model_path="Pekkapuuma/fulldata_for_9_epochs"):
        self.model = CLIPModel.from_pretrained(model_path)
        self.processor = CLIPProcessor.from_pretrained(model_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        
    def get_text_embedding(self, text):
        """
        Get text embedding vector using CLIP
        """
        inputs = self.processor(text=text, return_tensors="pt", padding=True, truncation=True)
        # Move inputs to the same device as the model
        inputs = {k: v.to(self.device) for k, v in inputs.items() if k != "pixel_values"}
        
        # Get text features
        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)
            
        # Normalize the features
        text_features = text_features / text_features.norm(dim=1, keepdim=True)
        
        # Convert to numpy array and then to list
        text_embedding = text_features.cpu().numpy().tolist()[0]
        return text_embedding
    
    def get_image_embedding(self, image):
        """
        Get image embedding vector using CLIP
        """
        inputs = self.processor(images=image, return_tensors="pt")
        # Move inputs to the same device as the model
        inputs = {k: v.to(self.device) for k, v in inputs.items() if k != "input_ids" and k != "attention_mask"}
        
        # Get image features
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)
            
        # Normalize the features
        image_features = image_features / image_features.norm(dim=1, keepdim=True)
        
        # Convert to numpy array and then to list
        image_embedding = image_features.cpu().numpy().tolist()[0]
        return image_embedding