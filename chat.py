import requests
import chromadb
from sentence_transformers import SentenceTransformer
model=SentenceTransformer("all-MiniLM-L6-v2")
client=chromadb.PersistentClient(path="./chroma_db")
collection=client.get_collection("softworks_docs")
question = input("Ask about Softworks: ")
embedding=model.encode(question).tolist()
results=collection.query(
    query_embeddings=[embedding],
    n_results=5
)
context="\n".join(results["documents"][0])
prompt = f"""
You are a helpful assistant for Softworks Technologies.

Understand the user's intended meaning, even if the question
contains spelling mistakes, missing words, or different wording.

Use the website content below to answer.
If the content partially answers the question, provide the
supported information.
If the information is genuinely missing, say you could not
find it on the website. Do not invent facts.

Website content:
{context}

Question: {question}

Answer:
"""
response=requests.post(
     "http://localhost:11434/api/generate",
     json={"model":"llama3.2:1b","prompt":prompt,"stream":False},
     timeout=120
    
)
response.raise_for_status()
print("\nChatbot:", response.json()["response"])