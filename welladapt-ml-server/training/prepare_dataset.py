"""
Mental Health Dataset Preparation - Enhanced Version
Uses public datasets + synthetic data for better training
"""

import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split
from typing import List, Dict
import re

class MentalHealthDatasetBuilder:
    """
    Builds a larger mental health emotion dataset.
    """
    
    def __init__(self, output_dir: str = "training/data"):
        self.output_dir = output_dir
        self.emotions = ['stress', 'anxiety', 'depression', 'neutral', 'positive']
        
        os.makedirs(f"{output_dir}/raw", exist_ok=True)
        os.makedirs(f"{output_dir}/processed", exist_ok=True)
        os.makedirs(f"{output_dir}/splits", exist_ok=True)
    
    def create_large_synthetic_dataset(self) -> List[Dict]:
        """
        Create a MUCH larger synthetic dataset (500+ examples)
        """
        
        dataset = []
        
        # STRESS examples (100 examples)
        stress_templates = [
            # English templates
            "I'm stressed about {topic}",
            "The pressure of {topic} is overwhelming",
            "I can't handle {topic}",
            "{topic} is stressing me out",
            "I feel overwhelmed by {topic}",
            "Too much stress from {topic}",
            "I'm so stressed, I can't sleep because of {topic}",
            "The deadline for {topic} is killing me",
            "I have too much {topic} to handle",
            "I'm breaking down from {topic} stress",
            
            # Sinhala templates  
            "මට {topic} ගැන stress එකක්",
            "{topic} pressure එක handle කරන්න බෑ",
            "මට {topic} stress වෙනවා",
            "{topic} නිසා මට හරිම අමාරුයි",
            
            # Code-mixed templates
            "මට {topic} ගැන හරිම stress එකක්",
            "{topic} එක overwhelming වෙනවා",
            "මට {topic} handle කරන්න බෑ stress එකෙන්",
            "{topic} deadline එක එනවා stress වෙනවා",
        ]
        
        stress_topics = [
            "exams", "my upcoming test", "assignments", "finals", "coursework",
            "my grades", "studying", "projects", "presentations", "deadlines",
            "academic performance", "failing", "my GPA", "the workload",
            "පරීක්ෂණ", "assignment", "exam", "study", "grade"
        ]
        
        for template in stress_templates:
            for topic in stress_topics[:15]:  # Use subset to avoid too much repetition
                text = template.format(topic=topic)
                dataset.append({'text': text, 'label': 'stress'})
        
        # ANXIETY examples (100 examples)
        anxiety_templates = [
            "I'm anxious about {topic}",
            "I worry constantly about {topic}",
            "I feel nervous about {topic}",
            "{topic} makes me anxious",
            "I can't stop worrying about {topic}",
            "I'm scared about {topic}",
            "Anxiety about {topic} is taking over",
            "I feel panicked about {topic}",
            "My heart races when I think about {topic}",
            "I'm terrified of {topic}",
            
            "මට {topic} ගැන කනස්සල්ලක් තියෙනවා",
            "{topic} ගැන හිතාගෙන බය හිතෙනවා",
            "මට {topic} anxious feel වෙනවා",
            "{topic} ගැන worry වෙනවා",
        ]
        
        anxiety_topics = [
            "my future", "failing", "what others think", "making mistakes",
            "the unknown", "being judged", "social situations", "my career",
            "disappointing people", "not being good enough", "everything",
            "future", "career", "life", "අනාගතය"
        ]
        
        for template in anxiety_templates:
            for topic in anxiety_topics[:12]:
                text = template.format(topic=topic)
                dataset.append({'text': text, 'label': 'anxiety'})
        
        # DEPRESSION examples (100 examples)
        depression_templates = [
            "I feel sad and hopeless",
            "Nothing makes me happy anymore",
            "I feel {feeling}",
            "I'm tired of {topic}",
            "Life feels {feeling}",
            "I feel like giving up on {topic}",
            "I don't care about {topic} anymore",
            "{topic} feels pointless",
            "I can't find joy in {topic}",
            "I'm exhausted from {topic}",
            
            "මට හරිම දුකයි {topic}",
            "{feeling} feel වෙනවා",
            "මට {topic} ගැන කිසිම interest එකක් නෑ",
        ]
        
        depression_feelings = [
            "lonely", "empty", "hopeless", "worthless", "numb",
            "isolated", "helpless", "defeated", "broken", "lost",
            "meaningless", "pointless", "exhausted", "drained"
        ]
        
        depression_topics = [
            "everything", "life", "studying", "my situation", "myself",
            "the future", "trying", "existing", "going on"
        ]
        
        for template in depression_templates:
            for i in range(12):
                if '{feeling}' in template:
                    text = template.format(feeling=depression_feelings[i % len(depression_feelings)])
                elif '{topic}' in template:
                    text = template.format(topic=depression_topics[i % len(depression_topics)])
                else:
                    text = template
                dataset.append({'text': text, 'label': 'depression'})
        
        # NEUTRAL examples (100 examples)
        neutral_templates = [
            "I'm doing {state} today",
            "Just a {type} day",
            "I'm {state}",
            "Everything is {state}",
            "Things are {state}",
            "It's an {type} day",
            "Nothing special {happening}",
            "Just {activity}",
            
            "මම {state} ඉන්නවා",
            "{type} දවසක්",
            "හරි ඉන්නවා අද",
        ]
        
        neutral_states = ["okay", "fine", "alright", "normal", "average", "regular"]
        neutral_types = ["regular", "normal", "typical", "average", "ordinary"]
        neutral_activities = ["going through my routine", "doing my work", "studying as usual"]
        neutral_happening = ["happening", "going on", "to report"]
        
        for template in neutral_templates:
            for i in range(15):
                if '{state}' in template:
                    text = template.format(state=neutral_states[i % len(neutral_states)])
                elif '{type}' in template:
                    text = template.format(type=neutral_types[i % len(neutral_types)])
                elif '{activity}' in template:
                    text = template.format(activity=neutral_activities[i % len(neutral_activities)])
                elif '{happening}' in template:
                    text = template.format(happening=neutral_happening[i % len(neutral_happening)])
                else:
                    text = template
                dataset.append({'text': text, 'label': 'neutral'})
        
        # POSITIVE examples (100 examples)
        positive_templates = [
            "I'm feeling {feeling} today",
            "Things are {state}",
            "I'm {feeling} about {topic}",
            "I feel {feeling}",
            "I'm making progress with {topic}",
            "I can {action}",
            "{topic} went well today",
            "I'm proud of {achievement}",
            "I feel motivated about {topic}",
            
            "අද {feeling} feel වෙනවා",
            "මට {topic} ගැන {feeling}",
            "හොඳට යනවා {topic}",
        ]
        
        positive_feelings = [
            "better", "great", "good", "hopeful", "confident", "happy",
            "positive", "optimistic", "encouraged", "motivated", "proud"
        ]
        
        positive_states = ["looking up", "improving", "getting better", "going well"]
        positive_topics = ["my studies", "myself", "my progress", "things", "life"]
        positive_actions = ["handle this", "do this", "manage", "succeed", "improve"]
        positive_achievements = ["my progress", "myself", "my work", "what I did"]
        
        for template in positive_templates:
            for i in range(12):
                try:
                    if '{feeling}' in template and '{topic}' in template:
                        text = template.format(
                            feeling=positive_feelings[i % len(positive_feelings)],
                            topic=positive_topics[i % len(positive_topics)]
                        )
                    elif '{feeling}' in template:
                        text = template.format(feeling=positive_feelings[i % len(positive_feelings)])
                    elif '{state}' in template:
                        text = template.format(state=positive_states[i % len(positive_states)])
                    elif '{action}' in template:
                        text = template.format(action=positive_actions[i % len(positive_actions)])
                    elif '{achievement}' in template:
                        text = template.format(achievement=positive_achievements[i % len(positive_achievements)])
                    elif '{topic}' in template:
                        text = template.format(topic=positive_topics[i % len(positive_topics)])
                    else:
                        text = template
                    dataset.append({'text': text, 'label': 'positive'})
                except:
                    continue
        
        print(f"✅ Created {len(dataset)} synthetic examples")
        return dataset
    
    def augment_with_emojis(self, dataset: List[Dict]) -> List[Dict]:
        """Add emoji variations"""
        
        emoji_map = {
            'stress': ['😫', '😤', '😩', '😖', '🤯'],
            'anxiety': ['😰', '😨', '😱', '😖', '😟'],
            'depression': ['😢', '😭', '😔', '☹️', '😞'],
            'neutral': ['😐', '😑', '🙂'],
            'positive': ['😊', '🙂', '😄', '😃', '🤗']
        }
        
        augmented = dataset.copy()
        
        # Add emoji to 30% of examples
        for item in dataset:
            if len(augmented) < len(dataset) * 1.3:  # Augment by 30%
                label = item['label']
                if label in emoji_map:
                    emoji = emoji_map[label][len(augmented) % len(emoji_map[label])]
                    augmented.append({
                        'text': f"{item['text']} {emoji}",
                        'label': label
                    })
        
        print(f"✅ Augmented with emojis: {len(dataset)} → {len(augmented)}")
        return augmented
    
    def create_balanced_dataset(self, dataset: List[Dict]) -> pd.DataFrame:
        """Balance dataset"""
        
        df = pd.DataFrame(dataset)
        
        print("\n📊 Dataset Distribution BEFORE balancing:")
        print(df['label'].value_counts())
        
        # Balance
        min_samples = df['label'].value_counts().min()
        
        balanced_dfs = []
        for emotion in self.emotions:
            emotion_df = df[df['label'] == emotion].sample(n=min(min_samples, 150), random_state=42)
            balanced_dfs.append(emotion_df)
        
        balanced_df = pd.concat(balanced_dfs, ignore_index=True)
        balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        print(f"\n✅ Balanced Dataset: {len(balanced_df)} examples")
        print("\n📊 Dataset Distribution AFTER balancing:")
        print(balanced_df['label'].value_counts())
        
        return balanced_df
    
    def split_dataset(self, df: pd.DataFrame) -> tuple:
        """Split dataset"""
        
        train_df, temp_df = train_test_split(
            df, test_size=0.3, random_state=42, stratify=df['label']
        )
        
        val_df, test_df = train_test_split(
            temp_df, test_size=0.5, random_state=42, stratify=temp_df['label']
        )
        
        print(f"\n📊 Data Splits:")
        print(f"   Train: {len(train_df)} examples")
        print(f"   Validation: {len(val_df)} examples")
        print(f"   Test: {len(test_df)} examples")
        
        return train_df, val_df, test_df
    
    def save_datasets(self, train_df, val_df, test_df):
        """Save datasets"""
        
        train_df.to_csv(f"{self.output_dir}/splits/train.csv", index=False)
        val_df.to_csv(f"{self.output_dir}/splits/val.csv", index=False)
        test_df.to_csv(f"{self.output_dir}/splits/test.csv", index=False)
        
        train_df.to_json(f"{self.output_dir}/splits/train.json", orient='records', lines=True)
        val_df.to_json(f"{self.output_dir}/splits/val.json", orient='records', lines=True)
        test_df.to_json(f"{self.output_dir}/splits/test.json", orient='records', lines=True)
        
        label_map = {label: idx for idx, label in enumerate(self.emotions)}
        with open(f"{self.output_dir}/label_map.json", 'w') as f:
            json.dump(label_map, f, indent=2)
        
        print(f"\n✅ Datasets saved!")
    
    def build(self):
        """Build complete dataset"""
        
        print("\n" + "="*70)
        print("🏗️  Building ENHANCED Mental Health Dataset")
        print("="*70 + "\n")
        
        # Create large synthetic dataset
        print("📝 Creating large synthetic dataset...")
        synthetic_data = self.create_large_synthetic_dataset()
        
        # Augment with emojis
        print("\n🔄 Augmenting with emojis...")
        augmented_data = self.augment_with_emojis(synthetic_data)
        
        # Balance
        print("\n⚖️  Balancing dataset...")
        balanced_df = self.create_balanced_dataset(augmented_data)
        
        # Split
        print("\n✂️  Splitting dataset...")
        train_df, val_df, test_df = self.split_dataset(balanced_df)
        
        # Save
        print("\n💾 Saving datasets...")
        self.save_datasets(train_df, val_df, test_df)
        
        print("\n" + "="*70)
        print("✅ Enhanced Dataset Ready!")
        print("="*70 + "\n")
        
        return train_df, val_df, test_df

if __name__ == "__main__":
    builder = MentalHealthDatasetBuilder()
    train_df, val_df, test_df = builder.build()
    
    print("\n📋 Sample Data:")
    print(train_df.sample(10))