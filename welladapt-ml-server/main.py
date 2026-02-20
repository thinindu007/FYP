"""
WellAdapt ML Server - Main Application
FastAPI server for emotion detection in bilingual mental health chat
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import torch

# Import our custom modules
from app.models.emotion_detector import EmotionDetector
from app.utils.text_processor import TextProcessor
from app.routes import ml_endpoints

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for handling startup and shutdown.
    This replaces the deprecated @app.on_event("startup") logic.
    """
    print("\n" + "="*50)
    print(" WellAdapt ML Server Starting...")
    print("="*50 + "\n")
    
    # Check if CUDA (GPU) is available
    if torch.cuda.is_available():
        print(f" GPU detected: {torch.cuda.get_device_name(0)}")
    else:
        print(" Running on CPU (this is fine for prototype)")
    
    # Load text processor
    print("\n Loading text processor...")
    ml_endpoints.text_processor = TextProcessor()
    print(" Text processor loaded")
    
    # Load emotion detection model
    print("\n Loading emotion detection model...")
    print(" This may take 1-2 minutes on first run...")
    ml_endpoints.emotion_detector = EmotionDetector()
    print(" Emotion detector loaded")
    
    print("\n" + "="*50)
    print(" ML Server Ready!")
    print(" API Docs: http://localhost:8000/docs")
    print("="*50 + "\n")
    
    yield  # Server runs here
    
    # Shutdown logic can go here if needed
    print("Shutting down ML Server...")

# Create FastAPI app with lifespan handler
app = FastAPI(
    title="WellAdapt ML Server",
    description="Emotion detection API for bilingual mental health support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "service": "WellAdapt ML Server",
        "status": "running",
        "version": "1.0.0"
    }

# Include ML routes
app.include_router(ml_endpoints.router, prefix="/ml", tags=["Machine Learning"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")