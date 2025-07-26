import json
from sentence_transformers import SentenceTransformer # to vector
import chromadb

# Load  data
with open("comprehensive_goals_dataset.json", "r") as f:
    data = json.load(f)

# Format each record 
documents = []
for i, item in enumerate(data):
    text = f"""
Goal: {item['goal']}
Subgoal: {item['subgoal']}
Progress: {item['progress']}
Barrier: {item['barrier']}
Strategy: {item['strategy']}
Affirmation: {item['affirmation']}
Context: {item['context']}
Roadmap: {item['roadmap_step']}
Study Plan: {item['study_plan']}
Checkpoint: {item['checkpoint']}
Inspiration: {item['inspiration']}
Routine: {item['routine']}
Difficulty: {item['difficulty_level']}
Time: {item['time_commitment']}
Resources: {', '.join(item['resources_needed'])}
Metrics: {', '.join(item['success_metrics'])}
"""
    documents.append(text.strip()) #add text to document

# Create vector store
client = chromadb.Client()
collection = client.get_or_create_collection(name="goal_memories")

# Embed documents
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(documents).tolist()

# Store in ChromaDB
collection.add(documents=documents, embeddings=embeddings, ids=[f"id_{i}" for i in range(len(documents))])

print("Vector store created with", len(documents), "documents.")
