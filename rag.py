
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
client=chromadb.PersistentClient("./chroma_db")
collection=client.get_or_create_collection(
    name="softworks_docs"
)


# Create a local ChromaDB database
client = chromadb.PersistentClient(path="./chroma_db")

# Create or reuse a collection
collection = client.get_or_create_collection(
    name="softworks_docs"
)


def load_and_store_documents():
    file_path=Path("data/softworks.txt")
    text=file_path.read_text(encoding="utf-8")
    chunk_size=500
    overlap=50
    chunks=[
        text[i:i+chunk_size]
        for i in range(0,len(text),chunk_size-overlap)
    ]
    for start in range(0,len(chunks),50):
        batch=chunks[start:start+50]
        ids=[
            f"softworks_{i}"
            for i in range(start,start+len(batch))

        ]
        embeddings=model.encode(batch).tolist()
        collection.upsert(
            ids=ids,
            documents=batch,
            embeddings=embeddings
        )
    print("Website content stored in ChromaDB!")
    print("Total chunks:", len(chunks))

if __name__ == "__main__":
    load_and_store_documents()

