import os
import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Paths relative to project root (d:\Ai for good hackathon)
BEED_JSON_PATH = "disctrict json/beed_output.json"
INDEX_PATH = "final project/faiss_index"

def load_beed_data():
    """Loads the Beed district JSON content."""
    if not os.path.exists(BEED_JSON_PATH):
        print(f"Error: File not found at {BEED_JSON_PATH}")
        return None
    
    try:
        with open(BEED_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return None

def create_documents(data):
    """Converts the JSON text content into LangChain Documents."""
    documents = []
    
    # Extract the main text content
    text_content = data.get("text", "")
    
    if text_content:
        # Create a document for the full text
        # Metadata is crucial for filtering later
        doc = Document(
            page_content=text_content,
            metadata={"district": "Beed", "source": "beed.pdf"}
        )
        documents.append(doc)
    
    # Process tables if needed, but text usually contains the core info
    return documents

def build_index():
    print("Loading data...")
    data = load_beed_data()
    if not data:
        return

    print("Creating documents...")
    docs = create_documents(data)
    
    print(f"Splitting {len(docs)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    splits = text_splitter.split_documents(docs)
    print(f"Created {len(splits)} chunks.")

    print("Initializing Embeddings (getting model)...")
    # Using a local model so no API key needed for embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Creating FAISS index...")
    vectorstore = FAISS.from_documents(splits, embeddings)

    print(f"Saving index to {INDEX_PATH}...")
    vectorstore.save_local(INDEX_PATH)
    print("Done!")

if __name__ == "__main__":
    build_index()
