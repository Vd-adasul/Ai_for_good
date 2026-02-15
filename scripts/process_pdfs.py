import os
import json
import time
import glob
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from PyPDF2 import PdfReader
import pdfplumber
from unstract.llmwhisperer import LLMWhispererClientV2

# Load environment variables
load_dotenv()

# Configuration
DISTRICT_PDF_DIR = "district wise work"
INDEX_PATH = "final project/faiss_index"
LLMWHISPERER_API_KEY = os.getenv("LLMWHISPERER_API_KEY")

def is_scanned_pdf(pdf_path, threshold=50):
    """Returns True if scanned (very little extractable text)."""
    try:
        reader = PdfReader(pdf_path)
        text_len = 0
        for page in reader.pages[:3]:  # check first 3 pages
            text = page.extract_text()
            if text:
                text_len += len(text)
        return text_len < threshold
    except Exception:
        return True # Assume scanned if unreadable

def extract_text_digital(pdf_path):
    """Extracts text from digital PDF using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading digital PDF {pdf_path}: {e}")
    return text.strip()

def extract_scanned_llmwhisperer(pdf_path, api_key):
    """Extracts text from scanned PDF using LLMWhisperer."""
    if not api_key:
        print(f"Skipping {pdf_path} - No LLMWHISPERER_API_KEY found.")
        return ""
    
    print(f"Uploading {os.path.basename(pdf_path)} to LLMWhisperer...")
    try:
        client = LLMWhispererClientV2(
            base_url="https://llmwhisperer-api.us-central.unstract.com/api/v2",
            api_key=api_key,
        )
        result = client.whisper(file_path=pdf_path)
        whisper_hash = result["whisper_hash"]

        while True:
            status = client.whisper_status(whisper_hash=whisper_hash)
            if status["status"] == "processed":
                final = client.whisper_retrieve(whisper_hash=whisper_hash)
                return final["extraction"]["result_text"]
            elif status["status"] == "failed":
                print(f"LLMWhisperer failed for {pdf_path}")
                return ""
            time.sleep(2)
    except Exception as e:
        print(f"LLMWhisperer Error: {e}")
        return ""

def process_pdfs():
    """Iterates through PDFs, extracts text, and returns LangChain Documents."""
    documents = []
    
    # Find all PDFs in the directory
    pdf_files = glob.glob(os.path.join(DISTRICT_PDF_DIR, "*.pdf"))
    print(f"Found {len(pdf_files)} PDFs in {DISTRICT_PDF_DIR}")

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        district_name = os.path.splitext(filename)[0]
        print(f"\nProcessing {filename}...")
        
        text_content = ""
        
        if is_scanned_pdf(pdf_path):
            print("Detected as SCANNED. Using OCR...")
            text_content = extract_scanned_llmwhisperer(pdf_path, LLMWHISPERER_API_KEY)
        else:
            print("Detected as DIGITAL. Using standard extraction...")
            text_content = extract_text_digital(pdf_path)
            
        if text_content:
            # Create Document
            # We add district metadata for RAG filtering
            doc = Document(
                page_content=text_content,
                metadata={"district": district_name, "source": filename}
            )
            documents.append(doc)
            print(f"Successfully extracted {len(text_content)} chars from {filename}")
        else:
            print(f"Failed to extract meaningful text from {filename}")

    return documents

def build_index():
    print("Starting Data Processing Pipeline...")
    
    # 1. Extract Data
    docs = process_pdfs()
    
    if not docs:
        print("No documents produced. Exiting.")
        return

    print(f"\nSplitting {len(docs)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    splits = text_splitter.split_documents(docs)
    print(f"Created {len(splits)} chunks.")

    print("Initializing Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Creating FAISS index...")
    vectorstore = FAISS.from_documents(splits, embeddings)

    print(f"Saving index to {INDEX_PATH}...")
    vectorstore.save_local(INDEX_PATH)
    print("Done! Knowledge Base Updated.")

if __name__ == "__main__":
    build_index()
