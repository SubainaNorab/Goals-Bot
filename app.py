from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import chromadb
import google.generativeai as genai

# Initialize Google Gemini 
genai.configure(api_key="")  # api key
model_gemini = genai.GenerativeModel('gemini-1.5-flash-latest')  # Updated model name

# Initialize Flask and vector DB
app = Flask(__name__)
model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("goal_memories")

# Endpoint to receive user queries
@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json.get("query") # read query
    if not user_query:
        return jsonify({"error": "Query missing"}), 400

    # Get embedding of query and fetch similar documents
    query_embed = model.encode([user_query]).tolist()[0]
    result = collection.query(query_embeddings=[query_embed], n_results=3) # 3 similar
    
    # Handle empty results
    if not result["documents"][0]:
        memories = "No relevant memories found."
    else:
        memories = "\n\n".join(result["documents"][0])

    # Step 5: Prepare augmented prompt
    prompt = f"""
You are a goal assistant. Based on the user's question and the following memories, provide practical, helpful advice.

User's Question:
{user_query}

Relevant Memory:
{memories}
"""

    #  Use Google Gemini API
    try:
        response = model_gemini.generate_content(prompt)
        return jsonify({"response": response.text})
    
    except Exception as e:
        return jsonify({"error": f"Failed to generate response: {str(e)}"}), 500

# Endpoint to add memories for testing
@app.route("/add_memory", methods=["POST"])
def add_memory():
    memory_text = request.json.get("memory")
    if not memory_text:
        return jsonify({"error": "Memory text missing"}), 400
    
    # Generate embedding and add to collection
    embedding = model.encode([memory_text]).tolist()[0]
    collection.add(
        documents=[memory_text],
        embeddings=[embedding],
        ids=[f"memory_{collection.count() + 1}"]
    )
    
    return jsonify({"message": "Memory added successfully"})

if __name__ == "__main__":
    app.run(debug=True)