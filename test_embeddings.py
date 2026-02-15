import os
import sys

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')

print("Testing HuggingFaceEmbeddings with full error...")

try:
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("✓ Embeddings loaded successfully!")
except Exception as e:
    print(f"\n=== FULL ERROR MESSAGE ===")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\n=== FULL TRACEBACK ===")
    import traceback
    traceback.print_exc()
    
    # Write to file
    with open("embedding_error.txt", "w") as f:
        f.write(f"Error type: {type(e).__name__}\n")
        f.write(f"Error message: {str(e)}\n\n")
        f.write("Full traceback:\n")
        f.write(traceback.format_exc())
    
    print("\nError written to embedding_error.txt")
