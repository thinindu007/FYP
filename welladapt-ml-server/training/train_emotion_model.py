# """
# Fine-tune XLM-RoBERTa for Mental Health Emotion Detection
# Supports bilingual Sinhala-English code-mixed text
# """

# import torch
# from torch.utils.data import Dataset, DataLoader
# from transformers import (
#     AutoTokenizer,
#     AutoModelForSequenceClassification,
#     TrainingArguments,
#     Trainer,
#     EarlyStoppingCallback
# )
# import pandas as pd
# import json
# import numpy as np
# from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import datetime
# import os

# class MentalHealthDataset(Dataset):
#     """
#     PyTorch Dataset for mental health emotion classification.
#     """
    
#     def __init__(self, texts, labels, tokenizer, max_length=128):
#         self.texts = texts
#         self.labels = labels
#         self.tokenizer = tokenizer
#         self.max_length = max_length
    
#     def __len__(self):
#         return len(self.texts)
    
#     def __getitem__(self, idx):
#         text = str(self.texts[idx])
#         label = self.labels[idx]
        
#         # Tokenize text
#         encoding = self.tokenizer(
#             text,
#             add_special_tokens=True,
#             max_length=self.max_length,
#             padding='max_length',
#             truncation=True,
#             return_tensors='pt'
#         )
        
#         return {
#             'input_ids': encoding['input_ids'].flatten(),
#             'attention_mask': encoding['attention_mask'].flatten(),
#             'labels': torch.tensor(label, dtype=torch.long)
#         }

# class EmotionModelTrainer:
#     """
#     Trainer for mental health emotion detection model.
#     """
    
#     def __init__(
#         self,
#         model_name: str = "xlm-roberta-base",
#         output_dir: str = "training/models",
#         data_dir: str = "training/data/splits"
#     ):
#         self.model_name = model_name
#         self.output_dir = output_dir
#         self.data_dir = data_dir
        
#         # Create output directory
#         os.makedirs(output_dir, exist_ok=True)
#         os.makedirs(f"{output_dir}/checkpoints", exist_ok=True)
#         os.makedirs(f"{output_dir}/logs", exist_ok=True)
        
#         # Load label mapping
#         with open("training/data/label_map.json", 'r') as f:
#             self.label_map = json.load(f)
        
#         self.num_labels = len(self.label_map)
#         self.id2label = {v: k for k, v in self.label_map.items()}
        
#         print(f" Number of labels: {self.num_labels}")
#         print(f"  Labels: {list(self.label_map.keys())}")
    
#     def load_data(self):
#         """Load train, validation, and test datasets"""
        
#         print("\n Loading datasets...")
        
#         # Load CSV files
#         train_df = pd.read_csv(f"{self.data_dir}/train.csv")
#         val_df = pd.read_csv(f"{self.data_dir}/val.csv")
#         test_df = pd.read_csv(f"{self.data_dir}/test.csv")
        
#         # Convert labels to integers
#         train_labels = [self.label_map[label] for label in train_df['label']]
#         val_labels = [self.label_map[label] for label in val_df['label']]
#         test_labels = [self.label_map[label] for label in test_df['label']]
        
#         print(f" Train: {len(train_df)} examples")
#         print(f" Validation: {len(val_df)} examples")
#         print(f" Test: {len(test_df)} examples")
        
#         return (
#             train_df['text'].tolist(), train_labels,
#             val_df['text'].tolist(), val_labels,
#             test_df['text'].tolist(), test_labels
#         )
    
#     def prepare_model(self):
#         """Load tokenizer and model"""
        
#         print(f"\n Loading model: {self.model_name}")
        
#         # Load tokenizer
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
#         # Load model
#         self.model = AutoModelForSequenceClassification.from_pretrained(
#             self.model_name,
#             num_labels=self.num_labels,
#             id2label=self.id2label,
#             label2id=self.label_map
#         )
        
#         print(" Model and tokenizer loaded")
        
#         return self.tokenizer, self.model
    
#     def create_datasets(self, train_texts, train_labels, val_texts, val_labels):
#         """Create PyTorch datasets"""
        
#         train_dataset = MentalHealthDataset(
#             train_texts,
#             train_labels,
#             self.tokenizer
#         )
        
#         val_dataset = MentalHealthDataset(
#             val_texts,
#             val_labels,
#             self.tokenizer
#         )
        
#         return train_dataset, val_dataset
    
#     def compute_metrics(self, pred):
#         """Compute evaluation metrics"""
        
#         labels = pred.label_ids
#         preds = pred.predictions.argmax(-1)
        
#         # Calculate metrics
#         precision, recall, f1, _ = precision_recall_fscore_support(
#             labels, preds, average='weighted'
#         )
#         acc = accuracy_score(labels, preds)
        
#         return {
#             'accuracy': acc,
#             'f1': f1,
#             'precision': precision,
#             'recall': recall
#         }
    
#     def train(self, train_dataset, val_dataset):
#         """Train the model"""
        
#         print("\n  Starting training...")
        
#         # Training arguments
#         training_args = TrainingArguments(
#             output_dir=f"{self.output_dir}/checkpoints",
            
#             # Training hyperparameters
#             num_train_epochs=5,  # Increase for better results
#             per_device_train_batch_size=8,  # Adjust based on GPU memory
#             per_device_eval_batch_size=8,
#             learning_rate=2e-5,
#             weight_decay=0.01,
            
#             # Evaluation
#             eval_strategy="epoch",
#             save_strategy="epoch",
#             load_best_model_at_end=True,
#             metric_for_best_model="f1",
            
#             # Logging
#             logging_dir=f"{self.output_dir}/logs",
#             logging_steps=10,
            
#             # Early stopping
#             save_total_limit=2,
            
#             # Performance
#             fp16=torch.cuda.is_available(),  # Use mixed precision if GPU available
#         )
        
#         # Create trainer
#         trainer = Trainer(
#             model=self.model,
#             args=training_args,
#             train_dataset=train_dataset,
#             eval_dataset=val_dataset,
#             compute_metrics=self.compute_metrics,
#             callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
#         )
        
#         # Train
#         print("\n Training will take 5-15 minutes depending on your hardware...")
#         train_result = trainer.train()
        
#         # Save model
#         print("\n Saving final model...")
#         trainer.save_model(f"{self.output_dir}/final_model")
#         self.tokenizer.save_pretrained(f"{self.output_dir}/final_model")
        
#         # Save training metrics
#         metrics = train_result.metrics
#         trainer.log_metrics("train", metrics)
#         trainer.save_metrics("train", metrics)
        
#         print(" Training complete!")
        
#         return trainer
    
#     def evaluate(self, trainer, test_texts, test_labels):
#         """Evaluate on test set"""
        
#         print("\n Evaluating on test set...")
        
#         # Create test dataset
#         test_dataset = MentalHealthDataset(
#             test_texts,
#             test_labels,
#             self.tokenizer
#         )
        
#         # Evaluate
#         metrics = trainer.evaluate(test_dataset)
        
#         print("\n Test Results:")
#         print(f"   Accuracy: {metrics['eval_accuracy']:.4f}")
#         print(f"   F1 Score: {metrics['eval_f1']:.4f}")
#         print(f"   Precision: {metrics['eval_precision']:.4f}")
#         print(f"   Recall: {metrics['eval_recall']:.4f}")
        
#         # Get predictions for confusion matrix
#         predictions = trainer.predict(test_dataset)
#         preds = predictions.predictions.argmax(-1)
        
#         # Plot confusion matrix
#         self.plot_confusion_matrix(test_labels, preds)
        
#         return metrics
    
#     def plot_confusion_matrix(self, true_labels, pred_labels):
#         """Plot and save confusion matrix"""
        
#         cm = confusion_matrix(true_labels, pred_labels)
        
#         plt.figure(figsize=(10, 8))
#         sns.heatmap(
#             cm,
#             annot=True,
#             fmt='d',
#             cmap='Blues',
#             xticklabels=list(self.label_map.keys()),
#             yticklabels=list(self.label_map.keys())
#         )
#         plt.title('Confusion Matrix - Mental Health Emotion Detection')
#         plt.ylabel('True Label')
#         plt.xlabel('Predicted Label')
#         plt.tight_layout()
        
#         # Save
#         plt.savefig(f"{self.output_dir}/confusion_matrix.png", dpi=300)
#         print(f"\n Confusion matrix saved to: {self.output_dir}/confusion_matrix.png")
        
#         plt.close()
    
#     def run_full_training(self):
#         """Complete training pipeline"""
        
#         print("\n" + "="*70)
#         print(" Fine-Tuning XLM-RoBERTa for Mental Health Emotion Detection")
#         print("="*70)
        
#         # Step 1: Load data
#         train_texts, train_labels, val_texts, val_labels, test_texts, test_labels = self.load_data()
        
#         # Step 2: Prepare model
#         tokenizer, model = self.prepare_model()
        
#         # Step 3: Create datasets
#         print("\n Creating PyTorch datasets...")
#         train_dataset, val_dataset = self.create_datasets(
#             train_texts, train_labels,
#             val_texts, val_labels
#         )
        
#         # Step 4: Train
#         trainer = self.train(train_dataset, val_dataset)
        
#         # Step 5: Evaluate
#         metrics = self.evaluate(trainer, test_texts, test_labels)
        
#         # Step 6: Save metadata
#         metadata = {
#             'model_name': self.model_name,
#             'num_labels': self.num_labels,
#             'label_map': self.label_map,
#             'training_date': datetime.now().isoformat(),
#             'test_metrics': {
#                 'accuracy': float(metrics['eval_accuracy']),
#                 'f1': float(metrics['eval_f1']),
#                 'precision': float(metrics['eval_precision']),
#                 'recall': float(metrics['eval_recall'])
#             }
#         }
        
#         with open(f"{self.output_dir}/model_metadata.json", 'w') as f:
#             json.dump(metadata, f, indent=2)
        
#         print("\n" + "="*70)
#         print(" Training Pipeline Complete!")
#         print(f" Model saved to: {self.output_dir}/final_model")
#         print("="*70 + "\n")
        
#         return trainer, metrics

# if __name__ == "__main__":
#     # Create trainer
#     trainer_obj = EmotionModelTrainer(
#         model_name="xlm-roberta-base",  # Multilingual model
#         output_dir="training/models"
#     )
    
#     # Run training
#     trainer, metrics = trainer_obj.run_full_training()
    
#     print("\n Fine-tuning complete! Your model is ready to use.")
#     print("\n Next step: Update app/models/emotion_detector.py to use this model")
"""
Fine-tune XLM-RoBERTa for Mental Health Emotion Detection
Supports bilingual Sinhala-English code-mixed text
Optimized for high-accuracy student emotion detection
"""

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
import pandas as pd
import json
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class MentalHealthDataset(Dataset):
    """PyTorch Dataset for mental health emotion classification."""
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

class EmotionModelTrainer:
    """Trainer for mental health emotion detection model."""
    def __init__(self, model_name="xlm-roberta-base", output_dir="training/models", data_dir="training/data/splits"):
        self.model_name = model_name
        self.output_dir = output_dir
        self.data_dir = data_dir
        
        # Create directories
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/checkpoints", exist_ok=True)
        os.makedirs(f"{output_dir}/logs", exist_ok=True)
        
        # Load label mapping
        with open("training/data/label_map.json", 'r') as f:
            self.label_map = json.load(f)
        
        self.num_labels = len(self.label_map)
        self.id2label = {v: k for k, v in self.label_map.items()}

    def load_data(self):
        """Load datasets from splits."""
        train_df = pd.read_csv(f"{self.data_dir}/train.csv")
        val_df = pd.read_csv(f"{self.data_dir}/val.csv")
        test_df = pd.read_csv(f"{self.data_dir}/test.csv")
        
        train_labels = [self.label_map[label] for label in train_df['label']]
        val_labels = [self.label_map[label] for label in val_df['label']]
        test_labels = [self.label_map[label] for label in test_df['label']]
        
        return (
            train_df['text'].tolist(), train_labels,
            val_df['text'].tolist(), val_labels,
            test_df['text'].tolist(), test_labels
        )

    def prepare_model(self):
        """Load tokenizer and model."""
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name, 
            num_labels=self.num_labels, 
            id2label=self.id2label, 
            label2id=self.label_map
        )
        return self.tokenizer, self.model

    def create_datasets(self, train_texts, train_labels, val_texts, val_labels):
        """Convert lists to PyTorch Datasets."""
        train_dataset = MentalHealthDataset(train_texts, train_labels, self.tokenizer)
        val_dataset = MentalHealthDataset(val_texts, val_labels, self.tokenizer)
        return train_dataset, val_dataset

    def compute_metrics(self, pred):
        """Calculate evaluation metrics."""
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
        acc = accuracy_score(labels, preds)
        return {'accuracy': acc, 'f1': f1, 'precision': precision, 'recall': recall}

    def train(self, train_dataset, val_dataset):
        """Execute the training process."""
        print("\n Starting optimized training for WellAdapt Intelligence Layer...")
        
        training_args = TrainingArguments(
            output_dir=f"{self.output_dir}/checkpoints",
            num_train_epochs=12,              # Increased for bilingual convergence
            per_device_train_batch_size=16,   # Stable gradients for better accuracy
            per_device_eval_batch_size=16,
            learning_rate=3e-5,               # Optimized for transformer fine-tuning
            weight_decay=0.01,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="f1",
            logging_dir=f"{self.output_dir}/logs",
            logging_steps=10,
            save_total_limit=2,
            fp16=torch.cuda.is_available(),   # Accelerate if GPU exists
            group_by_length=True
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=self.compute_metrics,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
        )
        
        trainer.train()
        
        # Save final artifacts
        print(f"\n Saving final model to {self.output_dir}/final_model")
        trainer.save_model(f"{self.output_dir}/final_model")
        self.tokenizer.save_pretrained(f"{self.output_dir}/final_model")
        
        return trainer

    def evaluate(self, trainer, test_texts, test_labels):
        """Final evaluation on test set."""
        test_dataset = MentalHealthDataset(test_texts, test_labels, self.tokenizer)
        metrics = trainer.evaluate(test_dataset)
        
        print("\n Final Test Set Metrics:")
        print(f" Accuracy: {metrics['eval_accuracy']:.4f}")
        print(f" F1-Score: {metrics['eval_f1']:.4f}")
        
        # Confusion Matrix
        predictions = trainer.predict(test_dataset)
        preds = predictions.predictions.argmax(-1)
        self.plot_confusion_matrix(test_labels, preds)
        
        return metrics

    def plot_confusion_matrix(self, true_labels, pred_labels):
        """Generate and save confusion matrix visualization."""
        cm = confusion_matrix(true_labels, pred_labels)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=list(self.label_map.keys()),
                    yticklabels=list(self.label_map.keys()))
        plt.title('Bilingual Emotion Detection Accuracy')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.savefig(f"{self.output_dir}/confusion_matrix.png")
        plt.close()

    def run_full_training(self):
        """Orchestrate the full pipeline."""
        train_texts, train_labels, val_texts, val_labels, test_texts, test_labels = self.load_data()
        self.prepare_model()
        train_ds, val_ds = self.create_datasets(train_texts, train_labels, val_texts, val_labels)
        trainer = self.train(train_ds, val_ds)
        metrics = self.evaluate(trainer, test_texts, test_labels)
        
        # Save metadata for the API server
        metadata = {
            'training_completed': datetime.now().isoformat(),
            'model': self.model_name,
            'metrics': metrics
        }
        with open(f"{self.output_dir}/model_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
            
        return trainer

if __name__ == "__main__":
    trainer_obj = EmotionModelTrainer()
    trainer_obj.run_full_training()