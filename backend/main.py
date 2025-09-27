from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import List, Dict, Optional
import uuid
import logging
import json
from pydantic import BaseModel
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from processing.loader import load_document_text
from processing.chunker import chunk_text
from processing.embedder import embed_chunks
from processing.vector_store import vector_store_instance

from routers.search import router as search_router
from models.schemas import IntelligentSearchRequest, IntelligentSearchResponse, ChatCompletionRequest, ChatMessage
from dependencies import get_query_router
from services.query_router import QueryRouter
import time
from services.llm_services import get_public_ai_client
from services.llm_services import LLMService

from gantt.planner import SwissAIGanttPlanner, create_planner
from gantt.models import GanttRequest, APIGanttResponse, ModifyGanttRequest

load_dotenv()

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

# File tracking system
PROCESSED_FILES_DB = UPLOAD_DIR / "processed_files.json"

def load_processed_files() -> Dict:
    """Load the processed files database from JSON file."""
    if PROCESSED_FILES_DB.exists():
        try:
            with open(PROCESSED_FILES_DB, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading processed files database: {e}")
            return {"files": []}
    return {"files": []}

def save_processed_files(data: Dict):
    """Save the processed files database to JSON file."""
    try:
        with open(PROCESSED_FILES_DB, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving processed files database: {e}")

def add_processed_file(filename: str, file_id: str, file_size: int, chunks_added: int):
    """Add a processed file to the tracking database."""
    db = load_processed_files()
    
    # Check if file already exists by filename (avoid duplicates)
    existing_file = next((f for f in db["files"] if f["filename"] == filename), None)
    if existing_file:
        print(f"File already exists in tracking database: {filename}")
        return False  # File already tracked
    
    new_file = {
        "file_id": file_id,
        "filename": filename,
        "file_size": file_size,
        "upload_time": time.time(),
        "chunks_added": chunks_added,
        "status": "completed"
    }
    
    db["files"].append(new_file)
    save_processed_files(db)
    print(f"Added file to tracking database: {filename}")
    return True  # Successfully added

def remove_processed_file(file_id: str) -> bool:
    """Remove a processed file from the tracking database."""
    db = load_processed_files()
    original_count = len(db["files"])
    
    # Remove the file with matching file_id
    db["files"] = [f for f in db["files"] if f["file_id"] != file_id]
    
    if len(db["files"]) < original_count:
        save_processed_files(db)
        print(f"Removed file from tracking database: {file_id}")
        return True
    return False

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
            logger.info(f"Starting document processing for file: {file.filename}")
            logger.info(f"File content type: {file.content_type}")

            # Validate file type
            if file.content_type not in SUPPORTED_FILE_TYPES:
                error_message = f"Unsupported file type: {file.content_type}. Supported types are: {list(SUPPORTED_FILE_TYPES.keys())}"
                logger.error(error_message)
                errors.append({"filename": file.filename, "error": error_message})
                continue

            logger.info(f"File type validation passed")

            # Save file temporarily
            file_extension = SUPPORTED_FILE_TYPES[file.content_type]
            file_id = str(uuid.uuid4())
            unique_filename = f"{file_id}{file_extension}"
            file_path = UPLOAD_DIR / unique_filename
            
            logger.info(f"Saving file as: {unique_filename}")

            contents = await file.read()
            logger.info(f"File size: {len(contents)} bytes")
            
            if len(contents) == 0:
                error_message = "File is empty or could not be read"
                logger.error(error_message)
                errors.append({"filename": file.filename, "error": error_message})
                continue
                
            with open(file_path, "wb") as buffer:
                buffer.write(contents)
            logger.info(f"File saved successfully to: {file_path}")

            # Load and process the document using your modules
            logger.info(f"Loading document text from: {file.filename}")
            document_text = load_document_text(file_path, file.filename)
            if not document_text or not document_text.strip():
                error_message = "No text could be extracted from the document."
                logger.error(error_message)
                errors.append({"filename": file.filename, "error": error_message})
                continue
            
            logger.info(f"Document text loaded successfully (length: {len(document_text)} characters)")

            # Chunk the text
            logger.info(f"Chunking the document text...")
            chunks = chunk_text(document_text)
            logger.info(f"Text chunked into {len(chunks)} chunks")

            # Embed the chunks
            logger.info(f"Creating embeddings for {len(chunks)} chunks...")
            embeddings = embed_chunks(chunks)
            logger.info(f"Embeddings created successfully ({len(embeddings)} embeddings)")

            # Store in vector db
            logger.info(f"Storing chunks and embeddings in vector database...")
            metadatas = [{"filename": file.filename, "file_id": file_id} for _ in chunks]
            vector_store_instance.add_documents(chunks, embeddings, metadatas)
            logger.info(f"Documents stored successfully in vector database")

            total_chunks_added += len(chunks)
            processed_files.append({
                "file_id": file_id,
                "filename": file.filename,
                "chunks_added": len(chunks)
            })
            logger.info(f"Document processing for {file.filename} completed successfully!")
            
            # Add to processed files tracking database
            file_added = add_processed_file(file.filename, file_id, len(contents), len(chunks))
            if not file_added:
                # File was a duplicate, add to errors
                error_message = f"File '{file.filename}' already exists in the system."
                print(error_message)
                errors.append({"filename": file.filename, "error": error_message})
                continue
                
            print(f"Document processing for {file.filename} completed successfully!")

        except Exception as e:
            error_detail = f"An unexpected error occurred: {str(e)}"
            logger.error(f"Error processing {file.filename}: {error_detail}")
            errors.append({"filename": file.filename, "error": error_detail})
        finally:
            # Clean up the saved file
            if file_path and file_path.exists():
                try:
                    file_path.unlink()
                    logger.info(f"Temporary file cleaned up: {file_path}")
                except Exception as cleanup_error:
                    logger.warning(f"Failed to cleanup temporary file {file_path}: {cleanup_error}")

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

@app.post("/chat-completion")
async def chat_completion(request: ChatCompletionRequest):
    try:
        llm_service = LLMService()  # Uses default model from LLMService
        
        # Convert ChatMessage objects to dictionary format expected by LLMService
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Generate response using the LLM service
        response = await llm_service.generate_with_messages(
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": response["text"]
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "total_tokens": response["tokens_used"]
                },
                "model": llm_service.model  # Use the model from the service
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat completion: {str(e)}")

@app.get("/uploaded-files")
async def list_uploaded_files():
    try:
        # Get processed files from JSON tracking database
        db = load_processed_files()
        files = db.get("files", [])
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Processed files retrieved successfully",
                "files": files,
                "total_files": len(files)
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing processed files: {str(e)}")

@app.delete("/uploaded-files/{file_id}")
async def delete_processed_file(file_id: str):
    try:
        success = remove_processed_file(file_id)
        
        if success:
            return JSONResponse(
                status_code=200,
                content={
                    "message": f"File {file_id} removed successfully",
                    "file_id": file_id
                }
            )
        else:
            raise HTTPException(status_code=404, detail=f"File with ID {file_id} not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

class CulturalAlignRequest(BaseModel):
    text: str
    target_culture: str
    language: str

class ChatHistoryRequest(BaseModel):
    messages: List[ChatMessage]
    project_name: Optional[str] = None

@app.post("/cultural_align_text/")
async def cultural_align_text(request: CulturalAlignRequest):
    try:
        llm_client = get_public_ai_client()

        system_prompt = "You are a helpful assistant that improves text to align with specific cultural values and norms."

        prompt = (
            f"Create a version of the following text that is fluent and natural in this language: {request.language}. "
            f"Make sure the answer respects the values and norms of this culture:'{request.target_culture}'.\n\n"
            f"DO NOT SIMPLY TRANSLATE THE TEXT, but adapt it culturally and contextually.\n\n"
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

def get_planner() -> SwissAIGanttPlanner:
    """Dependency to get planner instance."""
    try:
        return create_planner()
    except ValueError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Configuration error: {str(e)}"
        )
    
@app.post("/make_plan", response_model=APIGanttResponse)
async def make_gantt_plan(
    request: ChatHistoryRequest,
    planner: SwissAIGanttPlanner = Depends(get_planner)
):
    """
    Convert a chat history to a business plan summary and then to a structured Gantt chart JSON.
    
    - **messages**: Chat history in standard format (role: "user"/"assistant", content: string)
    - **project_name**: Optional project name to use in the output
    """
    start_time = datetime.now()
    
    try:
        # Validate input
        if not request.messages or len(request.messages) == 0:
            raise HTTPException(status_code=400, detail="Chat history cannot be empty")
        
        # Convert chat history to a format suitable for LLM
        llm_client = get_public_ai_client()
        
        # Create a summary prompt from the chat history
        chat_context = "\n".join([
            f"{'User' if msg.role == 'user' else 'Assistant'}: {msg.content}"
            for msg in request.messages
        ])
        
        summary_prompt = f"""Please analyze the following chat conversation and create a concise business plan summary that captures the key project requirements, goals, and deliverables discussed.

Chat History:
{chat_context}

Please provide a structured business plan summary that includes:
1. Project overview and objectives
2. Key requirements and deliverables
3. Main phases or milestones
4. Any timeline considerations mentioned
5. Resources or team requirements discussed

Business Plan Summary:"""
        
        print(f"Generating business plan summary from chat history...")
        business_plan_summary = llm_client.simple_chat(summary_prompt)
        print(f"Business plan summary generated: {business_plan_summary[:200]}...")
        
        # Use the summary to generate Gantt plan
        gantt_data = planner.generate_gantt_plan(
            description=business_plan_summary, 
            project_name=request.project_name or "Project from Chat"
        )
        print(gantt_data)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return APIGanttResponse(
            success=True,
            gantt_plan=gantt_data,
            processing_time_seconds=processing_time,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        return APIGanttResponse(
            success=False,
            error=str(e),
            processing_time_seconds=processing_time,
            timestamp=datetime.now()
        )
    

@app.post("/convert", response_model=APIGanttResponse)
async def convert_to_gantt(
    request: GanttRequest, 
    planner: SwissAIGanttPlanner = Depends(get_planner)
):
    """
    Convert a business plan description to a structured Gantt chart JSON.
    
    - **description**: Text describing the business plan or project
    - **project_name**: Optional project name to use in the output
    """
    start_time = datetime.now()
    
    try:
        # Validate input
        if not request.description.strip():
            raise HTTPException(status_code=400, detail="Description cannot be empty")
        
        # Generate Gantt plan
        gantt_data = planner.generate_gantt_plan(
            description=request.description, 
            project_name=request.project_name
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return APIGanttResponse(
            success=True,
            gantt_plan=gantt_data,
            processing_time_seconds=processing_time,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        return APIGanttResponse(
            success=False,
            error=str(e),
            processing_time_seconds=processing_time,
            timestamp=datetime.now()
        )

@app.post("/modify_gantt", response_model=APIGanttResponse)
async def modify_gantt_plan(
    request: ModifyGanttRequest,
    planner: SwissAIGanttPlanner = Depends(get_planner)
):
    """
    Modify an existing Gantt plan based on a prompt/instruction.
    
    - **gantt_plan**: Existing Gantt plan data to modify (as dict)
    - **prompt**: Instructions for how to modify the plan
    """
    start_time = datetime.now()
    
    try:
        # Validate input
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Modification prompt cannot be empty")
        
        if not request.gantt_plan:
            raise HTTPException(status_code=400, detail="Gantt plan data cannot be empty")
        
        # Modify the Gantt plan using the planner
        modified_gantt_data = planner.modify_gantt_plan(
            existing_plan=request.gantt_plan,
            prompt=request.prompt
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return APIGanttResponse(
            success=True,
            gantt_plan=modified_gantt_data,
            processing_time_seconds=processing_time,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        return APIGanttResponse(
            success=False,
            error=str(e),
            processing_time_seconds=processing_time,
            timestamp=datetime.now()
        )
