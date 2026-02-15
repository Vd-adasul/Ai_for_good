import os
from typing import List, Optional
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def is_scanned_pdf(pdf_path: str, threshold: int = 50) -> bool:
    """Returns True if scanned (very little extractable text)."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        text_len = 0
        for page in reader.pages[:3]:  # check first 3 pages
            text = page.extract_text()
            if text:
                text_len += len(text)
        return text_len < threshold
    except Exception:
        return True # Assume scanned if unreadable

def extract_text_digital(pdf_path: str) -> str:
    """Extracts text from digital PDF using pdfplumber."""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading digital PDF {pdf_path}: {e}")
    return text.strip()

def extract_scanned_llmwhisperer(pdf_path: str, api_key: Optional[str]) -> str:
    """Extracts text from scanned PDF using LLMWhisperer (optional)."""
    if not api_key:
        print(f"Skipping {pdf_path} - No LLMWHISPERER_API_KEY found.")
        return ""
    
    try:
        from unstract.llmwhisperer import LLMWhispererClientV2
    except ImportError:
        print("llmwhisperer-client not installed. Skipping OCR.")
        return ""
    
    import time
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

def process_single_pdf(pdf_path: str, llm_whisperer_key: Optional[str] = None) -> List[Document]:
    """
    Process a single PDF file and return a list of LangChain Documents.
    This function handles both digital and scanned PDFs.
    """
    filename = os.path.basename(pdf_path)
    district_name = os.path.splitext(filename)[0] # Heuristic: Use filename as district/topic
    
    print(f"Processing {filename}...")
    
    text_content = ""
    
    if is_scanned_pdf(pdf_path):
        print("Detected as SCANNED. Using OCR/LLMWhisperer...")
        text_content = extract_scanned_llmwhisperer(pdf_path, llm_whisperer_key)
    else:
        print("Detected as DIGITAL. Using standard extraction...")
        text_content = extract_text_digital(pdf_path)
        
    if text_content:
        doc = Document(
            page_content=text_content,
            metadata={"district": district_name, "source": filename}
        )
        return [doc]
    else:
        print(f"Failed to extract meaningful text from {filename}")
        return []

def get_text_chunks(documents: List[Document]) -> List[Document]:
    """Splits documents into chunks suitable for RAG."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    splits = text_splitter.split_documents(documents)
    return splits
