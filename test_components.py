import os
import sys

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')

print("Testing individual components...")

# Test 1: Load embeddings
print("\n1. Loading HuggingFaceEmbeddings...")
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("✓ Embeddings loaded successfully!")
except Exception as e:
    print(f"✗ Embeddings failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Load FAISS
print("\n2. Loading FAISS vectorstore...")
try:
    from langchain_community.vectorstores import FAISS
    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("✓ FAISS loaded successfully!")
except Exception as e:
    print(f"✗ FAISS failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Load LLM
print("\n3. Loading ChatGroq...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    from langchain_groq import ChatGroq
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant")
    print("✓ LLM loaded successfully!")
except Exception as e:
    print(f"✗ LLM failed: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Testing Complete ===")
