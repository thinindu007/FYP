"""
WellAdapt ML Server - Main Application
FastAPI server for emotion detection in bilingual mental health chat
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import torch

# Import our custom modules
from app.models.emotion_detector import EmotionDetector
from app.utils.text_processor import TextProcessor
from app.routes import ml_endpoints

# Create FastAPI app
app = FastAPI(
    title="WellAdapt ML Server",
    description="Emotion detection API for bilingual mental health support",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc"  # ReDoc at http://localhost:8000/redoc
)

# Enable CORS (so Node.js backend can call this server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",  # Node.js backend
        "http://localhost:3000",  # React frontend (for testing)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """
    Load ML models when server starts.
    This happens once, not on every request.
    """
    print("\n" + "="*50)
    print("🚀 WellAdapt ML Server Starting...")
    print("="*50 + "\n")
    
    # Check if CUDA (GPU) is available
    if torch.cuda.is_available():
        print(f"🎮 GPU detected: {torch.cuda.get_device_name(0)}")
    else:
        print("💻 Running on CPU (this is fine for prototype)")
    
    # Load text processor
    print("\n📝 Loading text processor...")
    ml_endpoints.text_processor = TextProcessor()
    print("✅ Text processor loaded")
    
    # Load emotion detection model
    print("\n🤖 Loading emotion detection model...")
    print("⏳ This may take 1-2 minutes on first run...")
    ml_endpoints.emotion_detector = EmotionDetector()
    print("✅ Emotion detector loaded")
    
    print("\n" + "="*50)
    print("✅ ML Server Ready!")
    print("📖 API Docs: http://localhost:8000/docs")
    print("="*50 + "\n")

@app.get("/")
async def root():
    """Root endpoint - basic info"""
    return {
        "service": "WellAdapt ML Server",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "detect_emotion": "/ml/detect-emotion",
            "batch_detect": "/ml/batch-detect-emotion",
            "health": "/ml/health",
            "model_info": "/ml/model-info",
            "docs": "/docs"
        }
    }

# Include ML routes
app.include_router(ml_endpoints.router, prefix="/ml", tags=["Machine Learning"])

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Accept connections from any IP
        port=8000,
        reload=True,      # Auto-reload on code changes
        log_level="info"
    )