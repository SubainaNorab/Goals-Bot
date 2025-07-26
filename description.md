### **Purpose:**



This is a goal assistant web API that:



Accepts user questions (/ask)



Retrieves relevant past memories (from ChromeDB)



Sends them to Gemini with the user question



Returns helpful advice based on both



###  **Key Components:**

* Flask App
* 
* Web framework that handles HTTP requests (/ask, /add\_memory).
* 
* Google Gemini API
* 
* Used to generate smart responses based on user input and retrieved memory.
* 
* Model used: gemini-1.5-flash-latest
* 
* ChromaDB (Vector Store)
* 
* Stores memories (text) as vectors.
* 
* Allows semantic search using embeddings.
* 
* Retrieved using similarity search with the user query.
* 
* SentenceTransformer (Embedding Model)
* 
* "all-MiniLM-L6-v2" converts text (memories and queries) into vectors.





### **Flow of /ask Endpoint:**



* Receives a user query via POST.
* 
* Converts the query into an embedding.
* 
* Retrieves top 3 similar memories from ChromaDB.
* 
* Formats a prompt with query + memories.
* 
* Sends the prompt to Gemini.
* 
* Returns the response.

### 

### **Flow of /add\_memory Endpoint :**



* Receives a memory string via POST.
* 
* Converts it to an embedding.
* 
* Adds it to the Chroma collection.





