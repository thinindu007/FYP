"""
Evaluate and compare base vs fine-tuned model
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from sklearn.metrics import classification_report
import json

def evaluate_model(model_path, test_data_path, label_map_path):
    """Evaluate model on test set"""
    
    # Load model
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    
    # Load test data
    test_df = pd.read_csv(test_data_path)
    
    # Load label mapping
    with open(label_map_path, 'r') as f:
        label_map = json.load(f)
    
    id2label = {v: k for k, v in label_map.items()}
    
    # Predict
    predictions = []
    true_labels = []
    
    for _, row in test_df.iterrows():
        text = row['text']
        true_label = row['label']
        
        # Tokenize
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        # Predict
        with torch.no_grad():
            outputs = model(**inputs)
            pred_idx = torch.argmax(outputs.logits, dim=1).item()
        
        pred_label = id2label[pred_idx]
        
        predictions.append(pred_label)
        true_labels.append(true_label)
    
    # Print report
    print(classification_report(true_labels, predictions))
    
    return predictions, true_labels

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Evaluating Fine-Tuned Model")
    print("="*60 + "\n")
    
    predictions, true_labels = evaluate_model(
        model_path="training/models/final_model",
        test_data_path="training/data/splits/test.csv",
        label_map_path="training/data/label_map.json"
    )
    
    print("\n Evaluation complete!")