import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings

try:
    from app.core.rag import rag_engine
    print(f"\n=== RAG STATUS ===")
    print(f"LLM initialized: {rag_engine.llm is not None}")
    print(f"VectorStore initialized: {rag_engine.vectorstore is not None}")
    print(f"==================")
except Exception as e:
    print(f"\n=== FATAL ERROR ===")
    import traceback
    traceback.print_exc()
    print(f"==================")
    sys.exit(1)
