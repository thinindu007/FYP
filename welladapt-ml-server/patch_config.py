import json
import os

model_dir = "training/models/final_model"
config_path = os.path.join(model_dir, "config.json")

# Define the standard XLM-RoBERTa configuration for 5 labels
config_data = {
  "_name_or_path": "xlm-roberta-base",
  "architectures": [
    "XLMRobertaForSequenceClassification"
  ],
  "attention_probs_dropout_prob": 0.1,
  "bos_token_id": 0,
  "eos_token_id": 2,
  "hidden_act": "gelu",
  "hidden_dropout_prob": 0.1,
  "hidden_size": 768,
  "id2label": {
    "0": "stress",
    "1": "anxiety",
    "2": "depression",
    "3": "neutral",
    "4": "positive"
  },
  "label2id": {
    "stress": 0,
    "anxiety": 1,
    "depression": 2,
    "neutral": 3,
    "positive": 4
  },
  "initializer_range": 0.02,
  "intermediate_size": 3072,
  "layer_norm_eps": 1e-05,
  "max_position_embeddings": 514,
  "model_type": "xlm-roberta",
  "num_attention_heads": 12,
  "num_hidden_layers": 12,
  "output_past": True,
  "pad_token_id": 1,
  "position_embedding_type": "absolute",
  "transformers_version": "4.44.2",
  "type_vocab_size": 1,
  "use_cache": True,
  "vocab_size": 250002
}

if not os.path.exists(model_dir):
    print(f"Error: Folder {model_dir} not found!")
else:
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=2)
    print(f"Successfully created {config_path}")