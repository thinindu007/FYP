"""
FastAPI endpoints for ML operations
Handles emotion detection and text analysis requests
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import time

router = APIRouter()

# Will be set when app starts
emotion_detector = None
text_processor = None

class EmotionRequest(BaseModel):
    """
    Request model for emotion detection.
    
    Example:
        {
            "text": "I am feeling stressed about exams",
            "language": "en"
        }
    """
    text: str = Field(..., min_length=1, max_length=1000, description="Text to analyze")
    language: Optional[str] = Field("mixed", description="Language: 'en', 'si', or 'mixed'")

class EmotionResponse(BaseModel):
    """Response model for emotion detection"""
    success: bool
    data: Dict
    processing_time_ms: float

class BatchEmotionRequest(BaseModel):
    """Request model for batch emotion detection"""
    texts: List[str] = Field(..., max_items=10, description="List of texts (max 10)")
    language: Optional[str] = "mixed"

@router.post("/detect-emotion", response_model=EmotionResponse)
async def detect_emotion(request: EmotionRequest):
    start_time = time.time()
    
    try:
        # Step 1: Preprocess text
        preprocessed = text_processor.preprocess(request.text)
        
        # Step 2: Detect emotion with emoji context
        emotion_result = emotion_detector.detect_emotion(
            preprocessed['cleaned_text'],
            emoji_context=preprocessed['emojis']
        )
        
        # Step 3: Add preprocessing info
        emotion_result['preprocessing'] = {
            'original_length': len(request.text),
            'cleaned_length': len(preprocessed['cleaned_text']),
            'is_code_mixed': preprocessed['languages']['is_mixed'],
            'has_emojis': any(preprocessed['emojis'].values())
        }
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        return EmotionResponse(
            success=True,
            data=emotion_result,
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Emotion detection failed: {str(e)}"
        )

@router.post("/batch-detect-emotion")
async def batch_detect_emotion(request: BatchEmotionRequest):
    start_time = time.time()
    
    try:
        results = []
        
        for text in request.texts:
            preprocessed = text_processor.preprocess(text)
            emotion_result = emotion_detector.detect_emotion(
                preprocessed['cleaned_text'],
                emoji_context=preprocessed['emojis']
            )
            results.append({
                'text': text,
                'emotion': emotion_result
            })
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            'success': True,
            'data': {
                'results': results,
                'count': len(results)
            },
            'processing_time_ms': round(processing_time, 2)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch emotion detection failed: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Verifies that ML models are loaded and ready.
    """
    return {
        'status': 'healthy',
        'model_loaded': emotion_detector is not None,
        'processor_loaded': text_processor is not None,
        'service': 'WellAdapt ML Server'
    }

@router.get("/model-info")
async def model_info():
    """
    Get information about the loaded model.
    """
    return {
        'model_name': emotion_detector.model_name,
        'emotions': emotion_detector.emotion_labels,
        'supports_code_mixing': True,
        'supports_emoji_analysis': True,
        'max_text_length': 1000
    }