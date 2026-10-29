\# Technical Documentation — Softworks Technologies RAG Chatbot



\## 1. Project Overview



The Softworks Technologies RAG Chatbot is a question-answering application designed to respond to user questions using information collected from the Softworks Technologies website.



The application uses Retrieval-Augmented Generation (RAG). It retrieves relevant website content and provides it to a language model to generate a response.



The chatbot provides a browser-based user interface built with Streamlit.



\## 2. Project Objectives



\- Collect and process website content.

\- Divide text into smaller chunks for retrieval.

\- Generate vector embeddings for text chunks.

\- Store embeddings in ChromaDB.

\- Retrieve relevant content for user questions.

\- Generate responses using a locally running Ollama language model.

\- Provide an interactive user interface.

\- Reduce unsupported answers by instructing the model to use retrieved context.



\## 3. Technologies Used



| Technology | Purpose |

|---|---|

| Python | Main programming language |

| Requests | HTTP requests |

| BeautifulSoup | HTML content parsing |

| Sentence Transformers | Text embedding generation |

| all-MiniLM-L6-v2 | Embedding model |

| ChromaDB | Vector storage and similarity search |

| Ollama | Local language model runtime |

| llama3.2:1b | Language model |

| Streamlit | Web-based user interface |



\## 4. System Architecture



The application follows this workflow:



1\. Website content is collected from https://www.softworkstech.com/.

2\. The extracted content is saved locally.

3\. The text is divided into overlapping chunks.

4\. Sentence Transformers converts the chunks into embeddings.

5\. ChromaDB stores the embeddings and associated text.

6\. A user enters a question through the Streamlit interface.

7\. The question is converted into an embedding.

8\. ChromaDB retrieves relevant text chunks.

9\. The retrieved text is included as context in a prompt.

10\. Ollama generates a response.

11\. The response is displayed in the chatbot interface.



\## 5. Website Data Collection



The ingestion component uses Requests to retrieve website HTML and BeautifulSoup to parse the page content.



The extracted text is saved in `data/softworks.txt`.



The initial ingestion run collected approximately 10,175 characters. The actual content may change when the website is scraped again.



\## 6. Text Chunking



The collected text is divided into smaller overlapping chunks.



Current configuration:



\- Chunk size: 500 characters

\- Chunk overlap: 50 characters

\- Approximate number of chunks in the initial run: 23



Chunking helps the retrieval system identify relevant portions of website content instead of passing the entire website text to the language model.



\## 7. Embeddings and Vector Database



The Sentence Transformers model `all-MiniLM-L6-v2` converts text chunks and user questions into numerical vector representations called embeddings.



ChromaDB stores the chunk text and embeddings in a persistent collection named `softworks\_docs`.



When a user submits a question, the system searches for semantically similar chunks and retrieves the most relevant results.



The current chatbot configuration requests up to five results.



\## 8. Language Model Integration



The chatbot uses Ollama to run the `llama3.2:1b` language model locally.



The application sends a request to:



`http://localhost:11434/api/generate`



The prompt includes the user's question and the retrieved website content.



The model is instructed to answer using the supplied context and avoid inventing company information. Prompt instructions can reduce unsupported answers but cannot guarantee that every answer is correct.



\## 9. User Interface



The user interface is implemented with Streamlit in `app.py`.



It provides:



\- A browser-based chat interface.

\- Suggested questions.

\- A custom question input field.

\- A conversation history during the current session.

\- Responses generated using retrieved website content.



Users can interact with the chatbot through the browser without entering questions in the terminal.



\## 10. Main Project Files



| File or folder | Purpose |

|---|---|

| `app.py` | Streamlit chatbot interface and integrated response workflow |

| `ingest.py` | Website content collection |

| `rag.py` | Text chunking, embedding generation, and vector storage |

| `chat.py` | Terminal-based chatbot support script |

| `test\_search.py` | Retrieval testing |

| `requirements.txt` | Python dependencies |

| `data/softworks.txt` | Locally collected website text |

| `chroma\_db/` | Locally generated persistent vector database |

| `README.md` | Project overview and setup instructions |

| `docs/technical\_documentation.md` | Technical documentation |



\## 11. Setup and Execution



\### Prerequisites



\- Python

\- Git

\- Ollama

\- The Ollama model `llama3.2:1b`



\### Install dependencies



Activate the project's virtual environment and install the dependencies listed in `requirements.txt`.



\### Collect website content



Run:



`python ingest.py`



\### Build the vector database



Run:



`python rag.py`



\### Start the chatbot UI



Run:



`python -m streamlit run app.py`



Open the local URL displayed by Streamlit, usually:



`http://localhost:8501`



Ollama must be running and the requested model must be available.



\## 12. Testing



The following checks were performed during development:



\- Website text extraction completed.

\- Initial text collection contained approximately 10,175 characters.

\- ChromaDB was populated with 23 chunks.

\- The terminal chatbot returned a response to a question about company services.

\- The Streamlit interface was launched and tested.



Additional testing should cover different question wording, spelling mistakes, unsupported questions, and cases where the retrieved website content is insufficient.



These results describe the tests performed during development; they do not represent a complete formal test suite.



\## 13. Limitations



\- Answers depend on the website content collected by the ingestion process.

\- Website updates are not automatically reflected until ingestion is run again.

\- Retrieval quality can be affected by ambiguous questions or spelling mistakes.

\- The language model may produce incorrect or unsupported information.

\- Ollama must be installed and running locally.

\- Chat history is maintained in the current Streamlit session unless additional persistence is implemented.

\- A locally running chatbot is not automatically accessible through the public internet.



\## 14. Conclusion



The project demonstrates a Retrieval-Augmented Generation workflow combining website data extraction, text chunking, embeddings, vector search, a local language model, and a browser-based interface.



It provides a foundation for answering questions about Softworks Technologies using retrieved website information. The system should be evaluated with additional test cases before being considered production-ready.

