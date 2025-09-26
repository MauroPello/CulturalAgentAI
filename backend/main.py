from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import List, Dict
import uuid
import pandas as pd
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from processing.loader import load_document_text
from processing.chunker import chunk_text
from processing.embedder import embed_chunks
from processing.vector_store import vector_store_instance
from llm.llm import get_public_ai_client
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001", "*"],  # Add your frontend URLs and allow all origins for extension
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {"message": "Hello, World!"}

@app.post("/process-document/", response_model=Dict)
async def process_document_endpoint(file: UploadFile = File(...)):
    """
    Uploads a document, saves it, extracts text, chunks it, and returns the chunks.
    The original file is deleted after processing.
    """
    print(f"Starting document processing for file: {file.filename}")
    print(f"File content type: {file.content_type}")
    
    # Validate file type
    if file.content_type not in SUPPORTED_FILE_TYPES:
        print(f"Unsupported file type: {file.content_type}")
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}. Supported types are: {list(SUPPORTED_FILE_TYPES.keys())}")

    print(f"File type validation passed")
    
    # Save file temporarily
    file_extension = SUPPORTED_FILE_TYPES[file.content_type]
    file_id = str(uuid.uuid4())
    unique_filename = f"{file_id}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    print(f"Saving file as: {unique_filename}")

    try:
        contents = await file.read()
        print(f"File size: {len(contents)} bytes")
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        print(f"File saved successfully to: {file_path}")

        # Load and process the document using your modules
        print(f"Loading document text from: {file.filename}")
        document_text = load_document_text(file_path, file.filename)
        if not document_text or not document_text.strip():
            print(f"No text could be extracted from the document")
            raise HTTPException(status_code=400, detail="No text could be extracted from the document.")
        
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
        # Create metadata for each chunk
        metadatas = [{
            "filename": file.filename,
            "file_id": file_id
        } for _ in chunks]
        vector_store_instance.add_documents(chunks, embeddings, metadatas)
        print(f"Documents stored successfully in vector database")

        total_docs = vector_store_instance.get_count()
        print(f"Total documents in store: {total_docs}")
        print(f"Document processing completed successfully!")
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Document processed and stored successfully.",
                "file_id": file_id,
                "filename": file.filename,
                "chunks_added": len(chunks),
                "total_documents_in_store": total_docs
            }
        )

    except RuntimeError as e:
        print(f"Runtime error during processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Unexpected error during processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    finally:
        # 5. Clean up the saved file
        if file_path.exists():
            file_path.unlink()
            print(f"Temporary file cleaned up: {file_path}")
        else:
            print(f"Temporary file not found for cleanup: {file_path}")

@app.post("/query/")
async def query_index(request: QueryRequest):
    """
    Accepts a text query, embeds it, and retrieves the most relevant chunks from the vector store.
    """
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        # Embed the user's query
        query_embedding = embed_chunks([request.query])[0]

        # Query the vector store
        results = vector_store_instance.query(
            query_embedding=query_embedding,
            n_results=request.n_results
        )

        # Prepare the context from retrieved documents
        context_chunks = []
        if results and results.get('documents') and results['documents'][0]:
            context_chunks = results['documents'][0]
        
        context_string = "\n\n---\n\n".join(context_chunks)

        prompt_template = """
        You are a helpful assistant for the company. Use the following context to answer the question.
        If the answer is not found in the context, state that you don't have enough information.

        CONTEXT:
        {context}

        QUESTION:
        {question}

        ANSWER:
        """

        # Format the final prompt
        final_prompt = prompt_template.format(
            context=context_string,
            question=request.query
        )

        print(f"Final prompt prepared for LLM:\n{final_prompt}")

        # Use the LLM to generate a response
        try:
            llm_client = get_public_ai_client()
            ai_response = llm_client.simple_chat(final_prompt)
            print(f"LLM response received: {ai_response}")

            return JSONResponse(status_code=200, content={
                "query": request.query,
                "answer": ai_response,
                "retrieved_chunks": context_chunks,
                "context_used": len(context_chunks) > 0
            })
        except Exception as llm_error:
            print(f"Error with LLM client: {str(llm_error)}")
            # If LLM fails, return the prepared prompt as fallback
            return JSONResponse(status_code=200, content={
                "query": request.query,
                "prepared_prompt": final_prompt,
                "retrieved_chunks": context_chunks,
                "error": f"LLM unavailable: {str(llm_error)}"
            })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during query: {str(e)}")


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