"""
Emotion Detector - WellAdapt
"""

import torch
# Explicitly import the specific classes to avoid config/tokenizer factory errors
from transformers import AutoModelForSequenceClassification, XLMRobertaTokenizer, XLMRobertaForSequenceClassification
from typing import Dict, List
import json
import os

class EmotionDetector:
    """
    Fine-tuned XLM-RoBERTa model wrapper for:
    - Mental health conversations
    - Bilingual Sinhala-English code-mixed text
    - Academic stress contexts
    
    Emotions: stress, anxiety, depression, neutral, positive
    """
    
    def __init__(self, model_path: str = "training/models/final_model"):
        """
        Initialize the emotion detector.
        Uses specific XLMRoberta classes to bypass missing config.json errors.
        """
        print(f"Loading emotion detection model...")
        
        # Check if fine-tuned model exists
        if not os.path.exists(model_path):
            print(f"Fine-tuned model not found at {model_path}")
            print(f"Using base model instead. Run training first for better results!")
            model_path = "xlm-roberta-base"
            self.is_finetuned = False
            # If using base, we can use Auto classes, but for consistency we stick to specific ones
            self.tokenizer = XLMRobertaTokenizer.from_pretrained(model_path)
            self.model = XLMRobertaForSequenceClassification.from_pretrained(model_path, num_labels=5)
        else:
            print(f"Loading fine-tuned model from {model_path}")
            self.is_finetuned = True
            
            # THE FIX: Directly use the specific XLMRoberta classes. 
            # This ignores the 'model_type' check in the config factory.
            self.tokenizer = XLMRobertaTokenizer.from_pretrained(model_path)
            self.model = XLMRobertaForSequenceClassification.from_pretrained(model_path)
        
        # Set to evaluation mode
        self.model.eval()
        
        # Load metadata if available
        metadata_path = "training/models/model_metadata.json"
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                if 'test_metrics' in self.metadata:
                    print(f" Model F1 Score: {self.metadata['test_metrics']['f1']:.4f}")
            except Exception as e:
                print(f"Could not load metadata: {e}")
        
        # Emotion labels (must match the training label_map order)
        self.emotion_labels = ['stress', 'anxiety', 'depression', 'neutral', 'positive']
        
        print("Emotion detector ready!")
        print(f"Fine-tuned: {self.is_finetuned}")
    
    def detect_emotion(self, text: str, emoji_context: Dict = None) -> Dict:
        """
        Detect emotion from text with emoji context.
        """
        # Tokenize using the XLMRoberta specific tokenizer
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )
        
        # Get prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
        
        # Convert to probabilities
        probabilities = torch.softmax(logits, dim=1)[0]
        probs_dict = {
            label: float(prob) 
            for label, prob in zip(self.emotion_labels, probabilities)
        }
        
        # Get top emotion
        text_emotion_idx = torch.argmax(probabilities).item()
        text_emotion = self.emotion_labels[text_emotion_idx]
        text_confidence = float(probabilities[text_emotion_idx])
        
        # Emoji-text conflict detection
        mixed_feeling = False
        emoji_emotion = None
        
        if emoji_context and any(emoji_context.values()):
            emoji_emotion = max(emoji_context, key=emoji_context.get)
            
            conflict_pairs = [
                ('positive', 'sad'),
                ('positive', 'anxious'),
                ('neutral', 'sad'),
            ]
            
            for text_emo, emoji_emo in conflict_pairs:
                if text_emotion == text_emo and emoji_emotion == emoji_emo:
                    mixed_feeling = True
                    break
        
        return {
            'emotion': text_emotion,
            'confidence': round(text_confidence, 3),
            'all_emotions': {label: round(prob, 3) for label, prob in probs_dict.items()},
            'mixed_feeling': mixed_feeling,
            'emoji_emotion': emoji_emotion if mixed_feeling else None,
            'explanation': self._generate_explanation(text_emotion, text_confidence, mixed_feeling, emoji_emotion),
            'model_version': 'fine-tuned' if self.is_finetuned else 'base'
        }
    
    def _generate_explanation(self, emotion: str, confidence: float, mixed: bool, emoji_emotion: str) -> str:
        if mixed:
            return f"Mixed signals: text suggests '{emotion}' but emojis hint at '{emoji_emotion}'."
        
        if confidence > 0.8:
            return f"Strong {emotion} detected."
        elif confidence > 0.6:
            return f"Moderate {emotion} detected."
        else:
            return f"Emotion detected as {emotion}, but signal is weak."

    def batch_detect(self, texts: List[str]) -> List[Dict]:
        return [self.detect_emotion(text) for text in texts]