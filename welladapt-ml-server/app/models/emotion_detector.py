"""
Emotion Detector using Multilingual BERT (mBERT)
Handles Sinhala-English code-mixed text for emotion classification
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, List
import numpy as np

class EmotionDetector:
    """
    Multilingual emotion detection model.
    
    Uses mBERT (Multilingual BERT) which supports 104 languages including:
    - English
    - Sinhala (partial support)
    - And handles code-mixed text reasonably well
    
    Emotions detected:
    - stress (exam stress, academic pressure)
    - anxiety (worry, fear)
    - sadness (depression, loneliness)
    - neutral (calm, okay)
    - happiness (joy, contentment)
    """
    
    def __init__(self, model_name: str = "bert-base-multilingual-cased"):
        """
        Initialize the emotion detector.
        
        Args:
            model_name: Hugging Face model identifier
                       Default: mBERT (supports 104 languages)
        """
        print(f"🤖 Loading emotion detection model: {model_name}")
        
        # Load tokenizer (converts text to numbers)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # For prototype: Use mBERT and fine-tune it ourselves
        # In production: You'd load a fine-tuned model
        self.model_name = model_name
        
        # We'll use a simple approach for the prototype
        # Load a pre-trained sentiment model and adapt it
        try:
            # Try to load emotion-specific model if available
            self.model = AutoModelForSequenceClassification.from_pretrained(
                "j-hartmann/emotion-english-distilroberta-base"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(
                "j-hartmann/emotion-english-distilroberta-base"
            )
            print("✅ Loaded emotion-specific model")
        except:
            # Fallback to multilingual BERT
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=5  # 5 emotions
            )
            print("✅ Loaded multilingual BERT (will need fine-tuning)")
        
        # Set model to evaluation mode
        self.model.eval()
        
        # Emotion labels
        self.emotion_labels = [
            'stress',      # 0 - Academic stress, exam pressure
            'anxiety',     # 1 - Worry, nervousness
            'sadness',     # 2 - Depression, loneliness
            'neutral',     # 3 - Calm, okay
            'happiness'    # 4 - Joy, contentment
        ]
        
        print("✅ Emotion detector ready!")
    
    def detect_emotion(self, text: str, emoji_context: Dict = None) -> Dict:
        """
        Detect emotion from text with emoji context.
        
        This handles 'mixed feelings' by considering:
        1. Text sentiment (from words)
        2. Emoji sentiment (from emojis)
        3. Conflict detection (happy words + sad emoji = mixed)
        
        Args:
            text: Input text (can be code-mixed)
            emoji_context: Dictionary with emoji counts from TextProcessor
            
        Returns:
            Dictionary with emotion prediction and confidence
        """
        
        # Step 1: Tokenize text (convert to model input)
        inputs = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )
        
        # Step 2: Get model prediction
        with torch.no_grad():  # Don't calculate gradients (faster)
            outputs = self.model(**inputs)
            logits = outputs.logits
        
        # Step 3: Convert to probabilities
        probabilities = torch.softmax(logits, dim=1)[0]
        probs_dict = {
            label: float(prob) 
            for label, prob in zip(self.emotion_labels, probabilities)
        }
        
        # Step 4: Get top emotion from text
        text_emotion_idx = torch.argmax(probabilities).item()
        text_emotion = self.emotion_labels[text_emotion_idx]
        text_confidence = float(probabilities[text_emotion_idx])
        
        # Step 5: Check for emoji-text conflict (mixed feelings)
        mixed_feeling = False
        emoji_emotion = None
        
        if emoji_context and any(emoji_context.values()):
            # Get dominant emoji emotion
            emoji_emotion = max(emoji_context, key=emoji_context.get)
            
            # Check for conflict
            # Example: Happy words (text: happiness) + Sad emoji = Mixed
            conflict_pairs = [
                ('happiness', 'sad'),
                ('happiness', 'anxious'),
                ('neutral', 'sad'),
                ('neutral', 'anxious'),
            ]
            
            for text_emo, emoji_emo in conflict_pairs:
                if text_emotion == text_emo and emoji_emotion == emoji_emo:
                    mixed_feeling = True
                    break
        
        # Step 6: Build response
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
            )
        }
        
        return result
    
    def _generate_explanation(
        self, 
        emotion: str, 
        confidence: float, 
        mixed: bool, 
        emoji_emotion: str
    ) -> str:
        """
        Generate human-readable explanation of emotion detection.
        
        Args:
            emotion: Detected emotion from text
            confidence: Confidence score
            mixed: Whether mixed feeling detected
            emoji_emotion: Emotion from emojis (if mixed)
            
        Returns:
            Explanation string
        """
        if mixed:
            return (
                f"Detected mixed feelings: text suggests '{emotion}' "
                f"but emojis suggest '{emoji_emotion}'. "
                f"This might indicate complex emotions."
            )
        
        if confidence > 0.7:
            return f"Strong {emotion} detected with high confidence."
        elif confidence > 0.5:
            return f"Moderate {emotion} detected."
        else:
            return f"Weak {emotion} signal. Emotion is unclear."
    
    def batch_detect(self, texts: List[str]) -> List[Dict]:
        """
        Detect emotions for multiple texts at once (more efficient).
        
        Args:
            texts: List of input texts
            
        Returns:
            List of emotion predictions
        """
        results = []
        for text in texts:
            results.append(self.detect_emotion(text))
        return results