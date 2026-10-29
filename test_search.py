import chromadb
from sentence_transformers import SentenceTransformer
model=SentenceTransformer("all-MiniLM-L6-v2")
client=chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="softworks_docs")

question = input("Ask about Softworks Technologies: ")
question_embedding=model.encode(question).tolist()

results=collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)
for document in results["documents"][0]:
    print("\n--- Relevant Website Content ---")
    print(document)
