"""
Text Processor for Sinhala-English Code-Mixed Text
Handles preprocessing of bilingual messages for emotion detection
"""

import re
from typing import List, Dict

class TextProcessor:
    """
    Processes bilingual Sinhala-English code-mixed text for ML models.
    
    Features:
    - Cleans special characters while preserving Sinhala script
    - Handles emojis (important for emotion detection!)
    - Normalizes whitespace
    - Preserves code-mixing patterns
    """
    
    def __init__(self):
        # Common emoji patterns (happy, sad, etc.)
        self.emoji_patterns = {
            'happy': ['😊', '😄', '😃', '🙂', '😁', '🤗'],
            'sad': ['😢', '😔', '😞', '😭', '☹️', '🙁'],
            'angry': ['😠', '😡', '🤬', '😤'],
            'anxious': ['😰', '😨', '😱', '😖'],
            'neutral': ['😐', '😑']
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean text while preserving important features.
        
        Args:
            text: Raw input text (can be Sinhala, English, or mixed)
            
        Returns:
            Cleaned text ready for model processing
        """
        # Don't remove emojis - they're important for emotion!
        # Just remove excessive whitespace and special chars
        
        # Remove URLs
        text = re.sub(r'http\S+|www.\S+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove excessive punctuation (but keep some for sentiment)
        text = re.sub(r'([!?.]){3,}', r'\1\1', text)
        
        return text.strip()
    
    def detect_emojis(self, text: str) -> Dict[str, int]:
        """
        Detect emotion-related emojis in text.
        This helps with 'mixed feelings' detection.
        
        Args:
            text: Input text with possible emojis
            
        Returns:
            Dictionary with emoji emotion counts
        """
        emoji_counts = {
            'happy': 0,
            'sad': 0,
            'angry': 0,
            'anxious': 0,
            'neutral': 0
        }
        
        for emotion, emoji_list in self.emoji_patterns.items():
            for emoji in emoji_list:
                emoji_counts[emotion] += text.count(emoji)
        
        return emoji_counts
    
    def detect_language_mix(self, text: str) -> Dict[str, bool]:
        """
        Detect if text contains Sinhala, English, or both.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary indicating which languages are present
        """
        # Sinhala Unicode range: 0D80–0DFF
        has_sinhala = bool(re.search(r'[\u0D80-\u0DFF]', text))
        
        # English letters
        has_english = bool(re.search(r'[a-zA-Z]', text))
        
        return {
            'has_sinhala': has_sinhala,
            'has_english': has_english,
            'is_mixed': has_sinhala and has_english
        }
    
    def preprocess(self, text: str) -> Dict:
        """
        Full preprocessing pipeline.
        
        Args:
            text: Raw input text
            
        Returns:
            Dictionary with cleaned text and metadata
        """
        cleaned_text = self.clean_text(text)
        emoji_info = self.detect_emojis(text)
        language_info = self.detect_language_mix(text)
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'emojis': emoji_info,
            'languages': language_info
        }