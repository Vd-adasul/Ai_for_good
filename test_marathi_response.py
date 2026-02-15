import sys
import os
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.rag import rag_engine

def test_marathi():
    print("Testing Marathi Response...")
    query = "How to control pests on cotton?"
    print(f"Query: {query}")
    
    response = rag_engine.get_answer(query)
    print("\nResponse:")
    print(response)
    
    # Check for Devanagari range (approximate)
    has_devanagari = any('\u0900' <= char <= '\u097F' for char in response)
    
    if has_devanagari:
        print("\nSUCCESS: Response contains Marathi characters.")
        sys.exit(0)
    else:
        print("\nFAILURE: Response does NOT contain Marathi characters.")
        print(f"Response was: {response}")
        sys.exit(1)

if __name__ == "__main__":
    test_marathi()
