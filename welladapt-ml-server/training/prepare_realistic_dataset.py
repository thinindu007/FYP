# """
# Create more realistic mental health dataset with variations
# """

# import pandas as pd
# import json
# import random
# from sklearn.model_selection import train_test_split

# class RealisticDatasetBuilder:
    
#     def __init__(self):
#         self.emotions = ['stress', 'anxiety', 'depression', 'neutral', 'positive']
#         random.seed(42)
    
#     def create_realistic_examples(self):
        
#         examples = []
        
#         # Base templates with variations
#         stress_base = [
#             "I have {number} exams next week and I haven't started studying",
#             "The assignment deadline is {time} and I'm not ready",
#             "I'm so overwhelmed with {topic}",
#             "Can't handle the pressure from {source}",
#             "Too many {things} to do, not enough time",
#             "I have a lot of {topic} but I think I can manage",
#             "Feeling stressed about {topic}",
#             "The workload is {intensity} this week",
#             "I stayed up all night {activity} but still feel unprepared",
#             "Everyone seems to be doing better than me in {subject}",
#             "I don't know how to finish all this {task}",
#             "My {person} expect so much from me",
#             "I'm afraid I'll disappoint {person}",
#             "{topic} is really stressing me out right now",
#             "I can't stop thinking about {topic}",
            
#             # Code-mixed stress
#             "මට {topic} ගැන stress එකක්",
#             "Exam එක ළඟට එනවා prepared නෑ",
#             "මට handle කරන්න බෑ මේ pressure එක",
#             "Too much කරන්න තියෙනවා time නෑ",
#             "මම overwhelmed වෙනවා {topic} එකෙන්",
#             "{number} assignments ගොඩක් තියෙනවා stress එකක්",
#             "Deadline එක {time} stress වෙනවා",
#             "මට {topic} complete කරන්න බෑ වගේ",
#         ]
        
#         # Variables for stress
#         numbers = ["two", "three", "four", "five", "several", "many"]
#         times = ["tomorrow", "in two days", "this week", "soon", "next week"]
#         topics = ["everything", "my studies", "exams", "assignments", "projects", "coursework"]
#         sources = ["studies", "exams", "family", "expectations", "deadlines"]
#         things = ["assignments", "exams", "tasks", "projects", "responsibilities"]
#         activities = ["studying", "working", "preparing", "reviewing"]
#         subjects = ["math", "science", "studies", "courses"]
#         tasks = ["work", "assignments", "studying"]
#         persons = ["parents", "family", "teachers", "professors"]
#         intensities = ["heavy", "intense", "overwhelming", "too much"]
        
#         # Generate stress examples
#         for template in stress_base:
#             # Generate 5 variations of each template
#             for i in range(5):
#                 text = template
#                 if '{number}' in text:
#                     text = text.replace('{number}', random.choice(numbers))
#                 if '{time}' in text:
#                     text = text.replace('{time}', random.choice(times))
#                 if '{topic}' in text:
#                     text = text.replace('{topic}', random.choice(topics))
#                 if '{source}' in text:
#                     text = text.replace('{source}', random.choice(sources))
#                 if '{things}' in text:
#                     text = text.replace('{things}', random.choice(things))
#                 if '{activity}' in text:
#                     text = text.replace('{activity}', random.choice(activities))
#                 if '{subject}' in text:
#                     text = text.replace('{subject}', random.choice(subjects))
#                 if '{task}' in text:
#                     text = text.replace('{task}', random.choice(tasks))
#                 if '{person}' in text:
#                     text = text.replace('{person}', random.choice(persons))
#                 if '{intensity}' in text:
#                     text = text.replace('{intensity}', random.choice(intensities))
                
#                 examples.append({'text': text, 'label': 'stress'})
        
#         anxiety_base = [
#             "I'm so worried about {topic}",
#             "What if I {negative_outcome}?",
#             "I keep thinking about {worry}",
#             "I can't sleep because I'm so nervous about {topic}",
#             "My heart races every time I think about {topic}",
#             "I'm nervous about {topic}",
#             "Hope {positive_outcome} goes well",
#             "I wonder if I {action} enough",
#             "I feel sick to my stomach before {event}",
#             "My hands shake when I'm {feeling}",
#             "I get headaches from worrying about {topic}",
#             "I'm terrified of {fear}",
            
#             # Code-mixed anxiety
#             "මට {topic} ගැන කනස්සල්ලක් තියෙනවා",
#             "What if මට {negative_outcome}?",
#             "මට හිතෙනවා {worry} කියලා",
#             "{event} ගැන හිතද්දී nervous වෙනවා",
#             "මට {fear} කියලා බයක් හිතෙනවා",
#         ]
        
#         worries = ["all the things that could go wrong", "my performance", "the outcome", "what others think"]
#         negative_outcomes = ["fail", "can't do this", "mess up", "disappoint everyone", "don't pass"]
#         positive_outcomes = ["everything", "the exam", "the presentation", "things"]
#         actions = ["prepared", "studied", "worked", "practiced"]
#         events = ["presentations", "exams", "tests", "interviews"]
#         feelings = ["anxious", "nervous", "worried", "scared"]
#         fears = ["failing", "disappointing people", "making mistakes", "being judged"]
        
#         for template in anxiety_base:
#             for i in range(5):
#                 text = template
#                 if '{topic}' in text:
#                     text = text.replace('{topic}', random.choice(topics))
#                 if '{worry}' in text:
#                     text = text.replace('{worry}', random.choice(worries))
#                 if '{negative_outcome}' in text:
#                     text = text.replace('{negative_outcome}', random.choice(negative_outcomes))
#                 if '{positive_outcome}' in text:
#                     text = text.replace('{positive_outcome}', random.choice(positive_outcomes))
#                 if '{action}' in text:
#                     text = text.replace('{action}', random.choice(actions))
#                 if '{event}' in text:
#                     text = text.replace('{event}', random.choice(events))
#                 if '{feeling}' in text:
#                     text = text.replace('{feeling}', random.choice(feelings))
#                 if '{fear}' in text:
#                     text = text.replace('{fear}', random.choice(fears))
                
#                 examples.append({'text': text, 'label': 'anxiety'})
        
#         depression_base = [
#             "I don't feel like doing {activity} anymore",
#             "What's the point of {activity}?",
#             "I feel {negative_feeling} inside",
#             "Nothing makes me {positive_feeling}",
#             "I just want to {escape_activity} all day",
#             "I'm feeling {negative_feeling} lately",
#             "Things don't seem as {positive_adjective} as they used to be",
#             "I'm tired {intensity}",
#             "I used to love {activity} but now I can't {action}",
#             "I don't want to talk to {person}",
#             "I feel like I'm not good at {topic}",
            
#             # Code-mixed depression
#             "මට {activity} කරන්න feel වෙන්නේ නෑ",
#             "{activity} කරන එකේ point එක මොකද්ද?",
#             "{positive_feeling} feel වෙන්නේ නෑ කිසිම දෙයකින්",
#             "මට {negative_feeling}",
#             "මට {action} කරන්නත් අමාරුයි",
#         ]
        
#         activities = ["anything", "studying", "working", "trying", "going out", "socializing"]
#         negative_feelings = ["empty", "hopeless", "worthless", "numb", "down", "sad", "alone"]
#         positive_feelings = ["happy", "excited", "interested", "motivated", "joyful"]
#         positive_adjectives = ["fun", "interesting", "exciting", "meaningful", "enjoyable"]
#         escape_activities = ["sleep", "lie in bed", "stay home", "hide"]
#         action_words = ["focus", "concentrate", "enjoy it", "participate", "care"]
        
#         for template in depression_base:
#             for i in range(5):
#                 text = template
#                 if '{activity}' in text:
#                     text = text.replace('{activity}', random.choice(activities))
#                 if '{negative_feeling}' in text:
#                     text = text.replace('{negative_feeling}', random.choice(negative_feelings))
#                 if '{positive_feeling}' in text:
#                     text = text.replace('{positive_feeling}', random.choice(positive_feelings))
#                 if '{positive_adjective}' in text:
#                     text = text.replace('{positive_adjective}', random.choice(positive_adjectives))
#                 if '{escape_activity}' in text:
#                     text = text.replace('{escape_activity}', random.choice(escape_activities))
#                 if '{intensity}' in text:
#                     text = text.replace('{intensity}', random.choice(["all the time", "constantly", "always", "every day"]))
#                 if '{action}' in text:
#                     text = text.replace('{action}', random.choice(action_words))
#                 if '{person}' in text:
#                     text = text.replace('{person}', random.choice(["anyone", "people", "my friends", "others"]))
#                 if '{topic}' in text:
#                     text = text.replace('{topic}', random.choice(topics))
                
#                 examples.append({'text': text, 'label': 'depression'})
        
#         neutral_base = [
#             "I'm {neutral_state}",
#             "Nothing special {happening}",
#             "Just a {type} day",
#             "{type} day at university",
#             "Everything is going {state}",
            
#             # Code-mixed neutral
#             "මම {state} ඉන්නවා",
#             "{type} day එකක්",
#             "කිසිම විශේෂ දෙයක් {happening}",
#         ]
        
#         neutral_states = ["okay", "fine", "alright", "doing okay", "managing"]
#         types = ["normal", "regular", "typical", "ordinary", "average", "usual"]
#         states = ["as usual", "normally", "fine", "okay", "well enough"]
#         happenings = ["today", "happening", "going on", "to report", "right now"]
        
#         for template in neutral_base:
#             for i in range(10):  # More variations for neutral
#                 text = template
#                 if '{neutral_state}' in text:
#                     text = text.replace('{neutral_state}', random.choice(neutral_states))
#                 if '{type}' in text:
#                     text = text.replace('{type}', random.choice(types))
#                 if '{state}' in text:
#                     text = text.replace('{state}', random.choice(states))
#                 if '{happening}' in text:
#                     text = text.replace('{happening}', random.choice(happenings))
                
#                 examples.append({'text': text, 'label': 'neutral'})
        
#         positive_base = [
#             "I'm feeling {positive_feeling} today",
#             "Things are {positive_state}",
#             "I'm {positive_feeling} about {topic}",
#             "I feel {positive_feeling}",
#             "I'm making progress with {topic}",
#             "I can {positive_action}",
#             "{topic} went {positive_adverb} today",
#             "I'm proud of {achievement}",
#             "I feel motivated about {topic}",
            
#             # Code-mixed positive
#             "අද {positive_feeling} feel වෙනවා",
#             "මට {topic} ගැන {positive_feeling}",
#             "හොඳට යනවා {topic}",
#             "{positive_state} වෙනවා දේවල්",
#         ]
        
#         positive_feelings = ["better", "great", "good", "hopeful", "confident", "happy", "positive", "optimistic", "encouraged", "motivated"]
#         positive_states = ["looking up", "improving", "getting better", "going well", "working out"]
#         positive_actions = ["handle this", "do this", "manage", "succeed", "overcome this", "improve"]
#         achievements = ["my progress", "myself", "my work", "what I accomplished", "my improvement"]
#         positive_adverbs = ["well", "great", "perfectly", "smoothly", "successfully"]
        
#         for template in positive_base:
#             for i in range(5):
#                 text = template
#                 if '{positive_feeling}' in text:
#                     text = text.replace('{positive_feeling}', random.choice(positive_feelings))
#                 if '{positive_state}' in text:
#                     text = text.replace('{positive_state}', random.choice(positive_states))
#                 if '{topic}' in text:
#                     text = text.replace('{topic}', random.choice(topics))
#                 if '{positive_action}' in text:
#                     text = text.replace('{positive_action}', random.choice(positive_actions))
#                 if '{achievement}' in text:
#                     text = text.replace('{achievement}', random.choice(achievements))
#                 if '{positive_adverb}' in text:
#                     text = text.replace('{positive_adverb}', random.choice(positive_adverbs))
                
#                 examples.append({'text': text, 'label': 'positive'})
        
#         emojis = {
#             'stress': ['😫', '😤', '😩', '🤯'],
#             'anxiety': ['😰', '😨', '😱', '😟'],
#             'depression': ['😢', '😭', '😔', '☹️'],
#             'neutral': ['😐', '🙂'],
#             'positive': ['😊', '😄', '🎉', '✨']
#         }
        
#         # Add emojis to 20% of examples
#         original_count = len(examples)
#         for i in range(int(original_count * 0.2)):
#             item = random.choice(examples)
#             label = item['label']
#             if label in emojis:
#                 emoji = random.choice(emojis[label])
#                 examples.append({
#                     'text': f"{item['text']} {emoji}",
#                     'label': label
#                 })
        
#         print(f" Created {len(examples)} realistic examples")
#         return examples
    
#     def build(self):
#         """Build dataset"""
        
#         print("\n" + "="*70)
#         print("  Building Realistic Mental Health Dataset")
#         print("="*70 + "\n")
        
#         # Create examples
#         examples = self.create_realistic_examples()
        
#         # Convert to DataFrame
#         df = pd.DataFrame(examples)
        
#         # Show distribution
#         print("\n Dataset Distribution:")
#         print(df['label'].value_counts())
        
#         # Balance dataset (equal samples per class)
#         min_samples = df['label'].value_counts().min()
#         balanced_dfs = []
#         for emotion in self.emotions:
#             emotion_df = df[df['label'] == emotion].sample(n=min_samples, random_state=42)
#             balanced_dfs.append(emotion_df)
        
#         df = pd.concat(balanced_dfs, ignore_index=True)
#         df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
#         print(f"\n Balanced to {len(df)} examples ({min_samples} per class)")
        
#         # Split
#         train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df['label'])
#         val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])
        
#         print(f"\n Splits: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")
        
#         # Save
#         import os
#         os.makedirs("training/data/splits", exist_ok=True)
        
#         train_df.to_csv("training/data/splits/train.csv", index=False)
#         val_df.to_csv("training/data/splits/val.csv", index=False)
#         test_df.to_csv("training/data/splits/test.csv", index=False)
        
#         # Save label map
#         label_map = {label: idx for idx, label in enumerate(self.emotions)}
#         with open("training/data/label_map.json", 'w') as f:
#             json.dump(label_map, f, indent=2)
        
#         print("\n Dataset saved!")
#         return train_df, val_df, test_df

# if __name__ == "__main__":
#     builder = RealisticDatasetBuilder()
#     builder.build()
"""
Create more realistic mental health dataset with variations
Includes dedicated Sinhala, English, and Code-Mixed support
"""

import pandas as pd
import json
import random
import os
from sklearn.model_selection import train_test_split

class RealisticDatasetBuilder:
    
    def __init__(self):
        self.emotions = ['stress', 'anxiety', 'depression', 'neutral', 'positive']
        random.seed(42)
    
    def create_realistic_examples(self):
        examples = []
        
        # --- Variables for dynamic replacement ---
        topics = ["exams", "my studies", "assignments", "projects", "finals", "GPA", "results"]
        sinhala_topics = ["විභාග", "assignment", "වැඩ", "ප්‍රතිඵල", "coursework"]
        negative_outcomes = ["fail", "mess up", "disappoint everyone", "can't do this"]
        times = ["tomorrow", "next week", "soon", "this week"]

        # --- STRESS: Overwhelmed, Pressure, Academic Load ---
        stress_templates = [
            # Failing Case Fix: Drowning/Think Straight
            "I'm drowning in {topic} and I can't even think straight",
            "I'm so overwhelmed with {topic}, the pressure is too much",
            "The workload of {topic} is heavy and I can't handle it",
            "Too much to do for {topic}, I'm losing my mind",
            
            # Pure Sinhala Stress (Fixing the Neutral bias)
            "වැඩ වැඩිකම නිසා මට පට්ටම මහන්සියි, මේක ඉවර කරගන්න බැරි වෙයි",
            "මට මේ {topic} එක නිසා මාරම stress එකක් තියෙන්නේ",
            "මේ වැඩ කන්දරාව මට දරාගන්න බැහැ, මම හිරවෙලා වගේ",
            "නිදි මරාගෙන වැඩ කරලත් වැඩ ඉවර වෙන්නේ නෑ, මට හරිම අමාරුයි",
            
            # Code-mixed
            "මට මේ assignment එක handle කරන්න බෑ, මම ගොඩක් overwhelmed",
            "Exam එක ළඟයි, මට මාරම stress එකක් feel වෙන්නේ",
            "I can't even think straight because of this {topic} ප්‍රශ්න"
        ]

        # --- ANXIETY: Worry, Physical Symptoms (Shaking), Fear of Future ---
        anxiety_templates = [
            # Failing Case Fix: Mess up/Shaking
            "What if I mess up the {topic}? My hands won't stop shaking",
            "I'm terrified of {topic}, I can't stop worrying about it",
            "My heart races every time I think about {topic} tomorrow",
            "I feel so panicked and nervous about {topic}",
            
            # Pure Sinhala Anxiety
            "{topic} එක ගැන හිතද්දී බඩ දඟලනවා වගේ දැනෙනවා, මට බයයි",
            "මට {topic} ගැන හිතද්දී හරිම බයයි, මොනවා වෙයිද මන්දා",
            "විභාගය ගැන හිතද්දී මට පිස්සු වගේ, හුස්ම ගන්නත් අමාරුයි",
            "අනාගතේ මොනවා වෙයිද කියලා මට ලොකු කනස්සල්ලක් තියෙනවා",
            
            # Code-mixed
            "What if මට {topic} එක කරගන්න බැරි වුණොත්? මට හරිම anxious",
            "Presentation එක ගැන හිතද්දී මගේ ඇඟ වෙව්ලනවා වගේ දැනෙනවා"
        ]

        # --- DEPRESSION/SADNESS: Hopelessness, Low Energy, Isolation ---
        depression_templates = [
            "I feel sad and hopeless, like nothing matters anymore",
            "I'm so drained, I don't want to do anything or talk to anyone",
            "Everything feels pointless lately, I'm just empty",
            "I used to love my studies but now I don't care at all",
            
            # Pure Sinhala Depression
            "මට හරිම දුකයි, කිසිම දෙයක් කරන්න හිතෙන්නේ නැහැ",
            "ජීවිතේ වැඩක් නැහැ වගේ දැනෙන්නේ, මට හරිම තනියම",
            "කිසිම දෙයකින් මට සතුටක් දැනෙන්නේ නැහැ දැන්",
            "මට හරිම කලකිරිලා ඉන්නේ හැමදේම ගැන",
            
            # Code-mixed
            "මට කිසිම දෙයක් කරන්න energy එකක් නෑ, feeling so down",
            "හරිම hopeless විදිහට තමයි මට දැන් feel වෙන්නේ"
        ]

        # --- NEUTRAL: Routine, Factual, Neither High nor Low ---
        neutral_templates = [
            "I'm doing okay, just a normal day at the university",
            "Nothing special happened today, just studying as usual",
            "It was a regular day, finished some work and went home",
            "I am managing my tasks fine for now",
            
            # Pure Sinhala Neutral
            "මම සාමාන්‍ය විදිහට ඉන්නවා අද",
            "කිසිම විශේෂ දෙයක් නැහැ, වැඩ ටික කරගත්තා",
            "අදත් වෙනදා වගේම තමයි, පාඩම් වැඩ ටික කළා",
            "දැනට ලොකු ප්‍රශ්නයක් නැහැ, වැඩ ටික යනවා",
            
            # Code-mixed
            "අද normal day එකක්, වැඩ ටික කරගත්තා",
            "මම fine, ලොකු විශේෂත්වයක් නෑ අද"
        ]

        # --- POSITIVE: Progress, Motivation, Achievement ---
        positive_templates = [
            "I'm feeling great! I finished my assignments early",
            "I'm very motivated to study today, feeling positive",
            "Things are looking up, I'm proud of my progress",
            "I can handle this! I'm confident about my exams",
            
            # Pure Sinhala Positive
            "මට අද ගොඩක් සතුටුයි, වැඩ ටික සාර්ථකව ඉවර කළා",
            "මට දැන් හොඳට දැනෙනවා, මම මගේ ගැන ආඩම්බරයි",
            "වැඩ ටික හොඳට යනවා, මට ලොකු විශ්වාසයක් තියෙනවා",
            "අද දවස හරිම හොඳයි, මම ගොඩක් motivated",
            
            # Code-mixed
            "මම හරිම happy අද, මම මගේ progress එක ගැන proud",
            "වැඩ ටික smoothly යනවා, feeling confident"
        ]

        # Map emotions to templates
        mapping = {
            'stress': stress_templates,
            'anxiety': anxiety_templates,
            'depression': depression_templates,
            'neutral': neutral_templates,
            'positive': positive_templates
        }

        # Generate examples (20 variations for each template)
        for label, templates in mapping.items():
            for template in templates:
                for _ in range(25): # Increased variation count
                    text = template.format(
                        topic=random.choice(topics + sinhala_topics),
                        time=random.choice(times)
                    )
                    examples.append({'text': text, 'label': label})

        # Add Emojis to 30% of data
        emoji_map = {
            'stress': ['😫', '🤯', '😖'],
            'anxiety': ['😰', '😨', '😱'],
            'depression': ['😢', '😔', '😞'],
            'neutral': ['😐', '🙂'],
            'positive': ['😊', '✨', '🔥']
        }
        
        for i in range(int(len(examples) * 0.3)):
            item = random.choice(examples)
            emoji = random.choice(emoji_map[item['label']])
            examples.append({'text': f"{item['text']} {emoji}", 'label': item['label']})

        return examples

    def build(self):
        print("\n" + "="*70)
        print("  Building ENHANCED Realistic Bilingual Dataset")
        print("="*70 + "\n")
        
        examples = self.create_realistic_examples()
        df = pd.DataFrame(examples)
        
        # Balance dataset
        min_samples = df['label'].value_counts().min()
        balanced_dfs = [df[df['label'] == e].sample(n=min_samples, random_state=42) for e in self.emotions]
        df = pd.concat(balanced_dfs, ignore_index=True).sample(frac=1, random_state=42)
        
        os.makedirs("training/data/splits", exist_ok=True)
        train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df['label'])
        val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])
        
        train_df.to_csv("training/data/splits/train.csv", index=False)
        val_df.to_csv("training/data/splits/val.csv", index=False)
        test_df.to_csv("training/data/splits/test.csv", index=False)
        
        label_map = {label: idx for idx, label in enumerate(self.emotions)}
        with open("training/data/label_map.json", 'w') as f:
            json.dump(label_map, f, indent=2)
        
        print(f" Dataset saved! Total examples: {len(df)}")
        return train_df, val_df, test_df

if __name__ == "__main__":
    builder = RealisticDatasetBuilder()
    builder.build()