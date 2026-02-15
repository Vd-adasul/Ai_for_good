from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from app.core.subsidy import subsidy_service
import os
import shutil

router = APIRouter()

# Setup templates - resolve relative to this file's location
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_APP_DIR = os.path.abspath(os.path.join(_THIS_DIR, ".."))
templates = Jinja2Templates(directory=os.path.join(_APP_DIR, "templates"))

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Admin dashboard to view and manage subsidies."""
    schemes = subsidy_service.get_all_schemes()
    return templates.TemplateResponse("admin.html", {"request": request, "schemes": schemes})

@router.post("/add_scheme")
async def add_scheme(
    category: str = Form(...),
    name: str = Form(...),
    benefit: str = Form(...),
    type: str = Form(...)
):
    """Endpoint to add a new subsidy scheme."""
    new_scheme = {
        "name": name,
        "benefit": benefit,
        "type": type
    }
    subsidy_service.add_scheme(category, new_scheme)
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin@1234" and password == "1234":
        return JSONResponse({"status": "success", "message": "Login successful"})
    return JSONResponse({"status": "error", "message": "Invalid credentials"}, status_code=401)

@router.post("/upload_district_data")
async def upload_district_data(file: UploadFile = File(...)):
    try:
        # Save to disk
        project_root = os.path.abspath(os.path.join(_APP_DIR, ".."))
        upload_dir = os.path.join(project_root, "district wise work")
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Update RAG
        # We need to import rag_engine appropriately. 
        # Since rag_engine is instantiated in app.core.rag, we can import it.
        from app.core.rag import rag_engine
        result = rag_engine.add_document(file_path)
        
        return JSONResponse({"status": "success", "message": f"File uploaded and processed: {result}"})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@router.post("/update_context")
async def update_context(context_text: str = Form(...)):
    try:
        project_root = os.path.abspath(os.path.join(_APP_DIR, ".."))
        context_file = os.path.join(project_root, "data", "additional_context.txt")
        os.makedirs(os.path.dirname(context_file), exist_ok=True)
        
        with open(context_file, "a", encoding="utf-8") as f:
            f.write(f"\n{context_text}")
            
        return JSONResponse({"status": "success", "message": "Context updated"})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
