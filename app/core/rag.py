import os
import traceback
import gc
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Resolve paths relative to this file's directory (app/core/rag.py)
# faiss_index is at <project_root>/faiss_index
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_THIS_DIR, "..", ".."))
INDEX_PATH = os.path.join(_PROJECT_ROOT, "faiss_index")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """You are an expert agricultural advisor for Maharashtra, India.
You specialize in drought contingency plans and helping farmers.

**Guidelines for Response:**
1.  **Language:** **STRICTLY MARATHI ONLY (देवनागरी लिपी)**.
    *   **TRANSLATE** all English information from the context into Marathi.
    *   Do NOT use English script or words.
    *   If a technical term is hard to translate, write it in Marathi script (e.g., 'Soybean' -> 'सोयाबीन').
2.  **Format:** Use **Markdown** for clarity.
    *   Use bullet points for lists.
    *   Use **bold** for important crop names or medicines.
    *   Keep paragraphs short (max 2-3 sentences).
3.  **Content:**
    *   Answer the specific question asked using the provided context.
    *   If the context is missing, say so honestly, but try to give general good advice if safe.
    *   Do NOT repeat the user's question.
    *   End with **one specific, actionable step** the farmer can take today.

**Context Usage:**
Use the provided `Context from agricultural documents` to answer. If the answer isn't there, state that.
"""

class RAGEngine:
    def __init__(self):
        self.vectorstore = None
        self.llm = None
        self._initialized = False

    def _ensure_initialized(self):
        """Lazy initialization — only loads models on first API call, not at startup.
        This lets the server bind its port quickly and avoids OOM during startup."""
        if self._initialized:
            return
        self._initialized = True  # Mark as attempted even if it fails
        
        if os.path.exists(INDEX_PATH):
            try:
                # Load Embeddings with minimal memory settings
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={"device": "cpu"},
                    encode_kwargs={"normalize_embeddings": True},
                )
                
                # Load FAISS
                self.vectorstore = FAISS.load_local(
                    INDEX_PATH, 
                    embeddings, 
                    allow_dangerous_deserialization=True
                )
                
                # Load LLM (lightweight — just an API client)
                if GROQ_API_KEY:
                    self.llm = ChatGroq(
                        groq_api_key=GROQ_API_KEY, 
                        model_name="llama-3.1-8b-instant"
                    )
                    print("RAG Engine Initialized Successfully.")
                else:
                    print("Warning: GROQ_API_KEY not found. RAG will not work.")
                
                # Force garbage collection after loading models
                gc.collect()
                
            except Exception as e:
                print(f"Error initializing RAG: {e}")
                print(f"Full traceback:\n{traceback.format_exc()}")
        else:
            print(f"Warning: FAISS index not found at {INDEX_PATH}. Run process_pdfs.py first.")

    def get_answer(self, query: str, context: str = "", history: list = []) -> str:
        """Retrieves answer from RAG using manual retrieve + LLM pattern with history."""
        # Lazy init on first call
        self._ensure_initialized()
        
        if not self.llm or not self.vectorstore:
            missing = []
            if not self.llm: missing.append("LLM")
            if not self.vectorstore: missing.append("VectorStore")
            return f"Systems are booting up... (RAG not initialized. Missing: {', '.join(missing)})"
        
        try:
            # 1. Retrieve relevant documents
            docs = self.vectorstore.similarity_search(query, k=3)
            
            # 1.5 Load static context
            try:
                context_file = os.path.join(_PROJECT_ROOT, "data", "additional_context.txt")
                if os.path.exists(context_file):
                    with open(context_file, "r", encoding="utf-8") as f:
                        static_context = f.read().strip()
                        if static_context:
                            context += f"\n\n[Permanent Admin Context]:\n{static_context}"
            except Exception as e:
                print(f"Error loading static context: {e}")
            
            # 2. Build prompt with retrieved context
            doc_texts = "\n\n---\n\n".join([doc.page_content for doc in docs])
            
            # Format history
            history_text = ""
            if history:
                history_text = "Previous Conversation:\n"
                for msg in history[-5:]: # Keep last 5 turns
                    role = "Farmer" if msg.get("role") == "user" else "Advisor"
                    history_text += f"{role}: {msg.get('content')}\n"
                history_text += "\n"

            prompt = f"""{SYSTEM_PROMPT}

{history_text}
Current Context from agricultural documents:
{doc_texts}

Additional real-time context: {context}

Farmer's question: {query}

Provide a helpful, practical answer in Markdown:"""
            
            # 3. Invoke LLM
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"RAG Error: {e}")
            return f"Error processing query: {e}"

    def add_document(self, file_path: str) -> str:
        """Adds a new PDF document to the RAG index dynamically."""
        self._ensure_initialized()
        try:
            from app.core.ingestion import process_single_pdf, get_text_chunks
            
            # 1. Process PDF
            docs = process_single_pdf(file_path)
            if not docs:
                return "Failed to extract text from PDF."
            
            # 2. Chunk
            chunks = get_text_chunks(docs)
            if not chunks:
                return "No content to add (empty PDF?)"
            
            # 3. Update Vector Store
            if self.vectorstore:
                self.vectorstore.add_documents(chunks)
                self.vectorstore.save_local(INDEX_PATH)
                return f"Successfully added {len(chunks)} new chunks to the Knowledge Base."
            else:
                # Initialize if not exists
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={"device": "cpu"},
                )
                self.vectorstore = FAISS.from_documents(chunks, embeddings)
                self.vectorstore.save_local(INDEX_PATH)
                return f"Initialized new Knowledge Base with {len(chunks)} chunks."
                
        except Exception as e:
            print(f"Error adding document: {e}")
            traceback.print_exc()
            return f"Error adding document: {str(e)}"

rag_engine = RAGEngine()
