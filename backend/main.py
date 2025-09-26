from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import List, Dict
import uuid
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from processing.loader import load_document_text
from processing.chunker import chunk_text
from processing.embedder import embed_chunks
from processing.vector_store import vector_store_instance

from routers.search import router as search_router
from models.schemas import IntelligentSearchRequest, IntelligentSearchResponse
from dependencies import get_query_router
from services.query_router import QueryRouter
import time
from services.llm_services import get_public_ai_client

app = FastAPI(
    title="Intelligent Document Processing API",
    description="AI-powered document processing with intelligent search routing",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
        "http://localhost:3001", 
        "http://127.0.0.1:3001"
    ],
    allow_origin_regex=r"^(chrome-extension|moz-extension)://.*",  # Allow browser extensions
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the intelligent search router
app.include_router(search_router)

# Keep your existing models for backward compatibility
class QueryRequest(BaseModel):
    query: str
    n_results: int = 5

# Uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

SUPPORTED_FILE_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-excel": ".xls",
    "text/plain": ".txt",
}

@app.get("/")
def read_root():
    return {"message": "Intelligent Document Processing API v2.0 - Now with smart search routing!"}

@app.post("/process-documents/", response_model=Dict)
async def process_documents_endpoint(files: List[UploadFile] = File(...)):
    """
    Uploads one or more documents, saves them, extracts text, chunks it, and stores it in the vector database.
    The original files are deleted after processing.
    """
    processed_files = []
    errors = []
    total_chunks_added = 0

    for file in files:
        file_path = None
        try:
            print(f"Starting document processing for file: {file.filename}")
            print(f"File content type: {file.content_type}")

            # Validate file type
            if file.content_type not in SUPPORTED_FILE_TYPES:
                error_message = f"Unsupported file type: {file.content_type}. Supported types are: {list(SUPPORTED_FILE_TYPES.keys())}"
                print(error_message)
                errors.append({"filename": file.filename, "error": error_message})
                continue

            print(f"File type validation passed")

            # Save file temporarily
            file_extension = SUPPORTED_FILE_TYPES[file.content_type]
            file_id = str(uuid.uuid4())
            unique_filename = f"{file_id}{file_extension}"
            file_path = UPLOAD_DIR / unique_filename
            
            print(f"Saving file as: {unique_filename}")

            contents = await file.read()
            print(f"File size: {len(contents)} bytes")
            with open(file_path, "wb") as buffer:
                buffer.write(contents)
            print(f"File saved successfully to: {file_path}")

            # Load and process the document using your modules
            print(f"Loading document text from: {file.filename}")
            document_text = load_document_text(file_path, file.filename)
            if not document_text or not document_text.strip():
                error_message = "No text could be extracted from the document."
                print(error_message)
                errors.append({"filename": file.filename, "error": error_message})
                continue
            
            print(f"Document text loaded successfully (length: {len(document_text)} characters)")

            # Chunk the text
            print(f"Chunking the document text...")
            chunks = chunk_text(document_text)
            print(f"Text chunked into {len(chunks)} chunks")

            # Embed the chunks
            print(f"Creating embeddings for {len(chunks)} chunks...")
            embeddings = embed_chunks(chunks)
            print(f"Embeddings created successfully ({len(embeddings)} embeddings)")

            # Store in vector db
            print(f"Storing chunks and embeddings in vector database...")
            metadatas = [{"filename": file.filename, "file_id": file_id} for _ in chunks]
            vector_store_instance.add_documents(chunks, embeddings, metadatas)
            print(f"Documents stored successfully in vector database")

            total_chunks_added += len(chunks)
            processed_files.append({
                "file_id": file_id,
                "filename": file.filename,
                "chunks_added": len(chunks)
            })
            print(f"Document processing for {file.filename} completed successfully!")

        except Exception as e:
            error_detail = f"An unexpected error occurred: {str(e)}"
            print(f"Error processing {file.filename}: {error_detail}")
            errors.append({"filename": file.filename, "error": error_detail})
        finally:
            # Clean up the saved file
            if file_path and file_path.exists():
                file_path.unlink()
                print(f"Temporary file cleaned up: {file_path}")

    total_docs = vector_store_instance.get_count()
    
    if not processed_files and errors:
        raise HTTPException(status_code=400, detail={"message": "All files failed to process.", "errors": errors})

    return JSONResponse(
        status_code=200,
        content={
            "message": "Document processing finished.",
            "processed_files": processed_files,
            "errors": errors,
            "total_chunks_added": total_chunks_added,
            "total_documents_in_store": total_docs
        }
    )

@app.post("/ask", response_model=IntelligentSearchResponse)
async def ask_intelligent(request: IntelligentSearchRequest, query_router: QueryRouter = Depends(get_query_router)):
    """
    The main endpoint for asking questions. It uses the QueryRouter to analyze,
    search, and generate a response.
    """
    start_time = time.time()
    
    final_response, results, analysis, tokens_used = await query_router.process_query(request.query)
    
    execution_time = time.time() - start_time
    
    return IntelligentSearchResponse(
        query=request.query,
        strategy_used=analysis.strategy,
        confidence=analysis.confidence,
        answer=final_response,
        sources=results,
        analysis=analysis,
        execution_time=execution_time,
        tokens_used=tokens_used
    )

@app.get("/uploaded-files")
async def list_uploaded_files():
    try:
        files = []
        # Include both PDF and Excel files
        for pattern in ["*.pdf", "*.xlsx", "*.xls", "*.xlsm"]:
            for file_path in UPLOAD_DIR.glob(pattern):
                file_stats = file_path.stat()
                files.append({
                    "filename": file_path.name,
                    "file_size": file_stats.st_size,
                    "upload_time": file_stats.st_mtime,
                    "file_path": str(file_path),
                    "file_type": file_path.suffix
                })
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Files retrieved successfully",
                "files": files,
                "total_files": len(files)
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

class CulturalAlignRequest(BaseModel):
    text: str
    target_culture: str
    language: str

@app.post("/cultural_align_text/")
async def cultural_align_text(request: CulturalAlignRequest):
    try:
        llm_client = get_public_ai_client()
        prompt = (
            f"Create a version of the following text that is more aligned with the culture {request.target_culture}. "
            f"It should be in the language '{request.language}'.\n\n"
            f"TEXT:\n{request.text}\n\n"
            "BETTER VERSION:"
        )
        print(f"Prompt for cultural alignment:\n{prompt}")
        better_version = llm_client.simple_chat(prompt)
        print(f"Better version generated:\n{better_version}")
        return JSONResponse(status_code=200, content={
            "text": request.text,
            "target_culture": request.target_culture,
            "language": request.language,
            "better_version": better_version
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing text: {str(e)}")
