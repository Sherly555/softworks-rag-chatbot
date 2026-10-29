
import streamlit as st
import requests
import chromadb
from sentence_transformers import SentenceTransformer


st.set_page_config(page_title="Softworks Chatbot", page_icon="💬")
st.title("Softworks Technologies Chatbot")
st.write(
    "Select a suggested question below or type your own question "
    "to explore information about Softworks Technologies."
)


@st.cache_resource
def load_resources():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("softworks_docs")
    return model, collection

model, collection = load_resources()


if "messages" not in st.session_state:
    st.session_state.messages = []


st.subheader("Suggested questions")

suggestions = [
    "What services does Softworks Technologies provide?",
    "Does Softworks provide dedicated developers?",
    "What is staff augmentation?",
    "Can Softworks help me build a digital product?",
    "How does Softworks help businesses?",
    "What technology solutions does Softworks offer?",
    "How can I contact Softworks Technologies for my project?"
]

# Display suggested questions in two columns
cols = st.columns(2)     
selected_question = None

for i, suggestion in enumerate(suggestions):
    with cols[i % 2]:
        if st.button(suggestion, key=f"suggestion_{i}"):
            selected_question = suggestion


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


typed_question = st.chat_input("Type your own question here...")


question = selected_question or typed_question

if question:
   
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    try:
        
        embedding = model.encode(question).tolist()

       
        results = collection.query(
            query_embeddings=[embedding],
            n_results=5
        )

        documents = results["documents"][0] if results["documents"] else []
        context = "\n".join(documents)

        
        prompt = f"""
You are a helpful assistant for Softworks Technologies.

Answer the user's question using the website content below.
Understand spelling mistakes and different ways of asking.
If the content does not contain the answer, say:
"I could not find this information in the available website content."
Do not invent company facts.

Website content:
{context}

Question: {question}

Answer:
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        answer = response.json()["response"]

    except requests.RequestException as error:
        answer = f"Could not connect to Ollama: {error}"

    except Exception as error:
        answer = f"An error occurred: {error}"

   
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)
