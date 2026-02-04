"""
Emotion Detector
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, List
import json
import os

class EmotionDetector:
    """
    fine-tuned XLM-RoBERTa modal.
    
    model for:
    - Mental health conversations
    - Bilingual Sinhala-English code-mixed text
    - Academic stress contexts
    
    Emotions: stress, anxiety, depression, neutral, positive
    """
    
    def __init__(self, model_path: str = "training/models/final_model"):
        """
        Initialize the emotion detector with fine-tuned model.
        
        """
        print(f"Loading fine-tuned emotion detection model...")
        
        # Check if fine-tuned model exists
        if not os.path.exists(model_path):
            print(f"Fine-tuned model not found at {model_path}")
            print(f"Using base model instead. Run training first for better results!")
            model_path = "xlm-roberta-base"
            self.is_finetuned = False
        else:
            print(f"Loading fine-tuned model from {model_path}")
            self.is_finetuned = True
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        
        # Set to evaluation mode
        self.model.eval()
        
        # Load metadata if available
        metadata_path = "training/models/model_metadata.json"
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            print(f" Model F1 Score: {self.metadata['test_metrics']['f1']:.4f}")
        
        # Emotion labels (from fine-tuning)
        self.emotion_labels = ['stress', 'anxiety', 'depression', 'neutral', 'positive']
        
        print("Emotion detector ready!")
        print(f"Fine-tuned: {self.is_finetuned}")
    
    def detect_emotion(self, text: str, emoji_context: Dict = None) -> Dict:
        """
        Detect emotion from text with emoji context.
        
        returns Dictionary with emotion prediction and details
        """
        
        # Tokenize
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
        
        # Check for emoji-text conflict
        mixed_feeling = False
        emoji_emotion = None
        
        if emoji_context and any(emoji_context.values()):
            emoji_emotion = max(emoji_context, key=emoji_context.get)
            
            # Conflict detection
            conflict_pairs = [
                ('positive', 'sad'),
                ('positive', 'anxious'),
                ('neutral', 'sad'),
            ]
            
            for text_emo, emoji_emo in conflict_pairs:
                if text_emotion == text_emo and emoji_emotion == emoji_emo:
                    mixed_feeling = True
                    break
        
        # Build result
        result = {
            'emotion': text_emotion,
            'confidence': round(text_confidence, 3),
            'all_emotions': {
                label: round(prob, 3) 
                for label, prob in probs_dict.items()
            },
            'mixed_feeling': mixed_feeling,
            'emoji_emotion': emoji_emotion if mixed_feeling else None,
            'explanation': self._generate_explanation(
                text_emotion, 
                text_confidence, 
                mixed_feeling, 
                emoji_emotion
            ),
            'model_version': 'fine-tuned' if self.is_finetuned else 'base'
        }
        
        return result
    
    def _generate_explanation(
        self, 
        emotion: str, 
        confidence: float, 
        mixed: bool, 
        emoji_emotion: str
    ) -> str:
        """Generate explanation of emotion detection"""
        
        if mixed:
            return (
                f"Detected mixed feelings: text suggests '{emotion}' "
                f"but emojis suggest '{emoji_emotion}'. "
                f"This might indicate complex emotions."
            )
        
        if confidence > 0.8:
            return f"Strong {emotion} detected with high confidence."
        elif confidence > 0.6:
            return f"Moderate {emotion} detected."
        else:
            return f"Weak {emotion} signal. Emotion is unclear."
    
    def batch_detect(self, texts: List[str]) -> List[Dict]:
        """Batch emotion detection"""
        results = []
        for text in texts:
            results.append(self.detect_emotion(text))
        return results