"""
Optimized Evaluation Script for WellAdapt
Handles batching, GPU support, and confusion matrix visualization
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
import json
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm  # For progress bars

def evaluate_model(model_path, test_data_path, label_map_path, batch_size=16):
    """
    Evaluates the model using GPU (if available) and batch processing.
    """
    # 1. Device Setup (Matches your training environment)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # 2. Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    model.eval()
    
    # 3. Load data and label map
    test_df = pd.read_csv(test_data_path)
    with open(label_map_path, 'r') as f:
        label_map = json.load(f)
    id2label = {v: k for k, v in label_map.items()}
    
    predictions = []
    true_labels = []
    
    # 4. Batch Processing (Significantly faster)
    print(f"Processing {len(test_df)} samples in batches of {batch_size}...")
    for i in tqdm(range(0, len(test_df), batch_size)):
        batch_df = test_df.iloc[i : i + batch_size]
        texts = batch_df['text'].tolist()
        batch_true = batch_df['label'].tolist()
        
        # Tokenize batch
        inputs = tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            # Get the highest probability indices
            pred_indices = torch.argmax(outputs.logits, dim=1).tolist()
        
        # Map indices back to labels
        batch_preds = [id2label[idx] for idx in pred_indices]
        
        predictions.extend(batch_preds)
        true_labels.extend(batch_true)
    
    # 5. Output Results
    print("\n" + "="*30)
    print("CLASSIFICATION REPORT")
    print("="*30)
    # Using 'macro' average is recommended for imbalanced code-mixed data
    print(classification_report(true_labels, predictions, digits=4))
    
    # 6. Confusion Matrix Visualization
    plot_confusion_matrix(true_labels, predictions, list(label_map.keys()))

    return predictions, true_labels

def plot_confusion_matrix(y_true, y_pred, labels):
    """Generates a visual heatmap to detect stress/sadness confusion."""
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.title('WellAdapt Emotion Detection: Predicted vs Actual')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.savefig('evaluation_results.png')
    print("\nConfusion matrix saved as 'evaluation_results.png'")
    plt.show()

if __name__ == "__main__":
    evaluate_model(
        model_path="training/models/final_model",
        test_data_path="training/data/splits/test.csv",
        label_map_path="training/data/label_map.json"
    )