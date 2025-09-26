from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
from pathlib import Path
import uuid
from typing import List

app = FastAPI()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Check if file is provided
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Check file size (limit to 10MB)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:  # 10MB in bytes
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB")
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = ".pdf"
    unique_filename = f"{file_id}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "PDF uploaded successfully",
                "file_id": file_id,
                "filename": file.filename,
                "saved_as": unique_filename,
                "file_size": len(contents),
                "file_path": str(file_path)
            }
        )
    
    except Exception as e:
        # Clean up file if something went wrong
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

@app.post("/upload-multiple-pdfs")
async def upload_multiple_pdfs(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    uploaded_files = []
    errors = []
    
    for file in files:
        try:
            # Check file extension
            if not file.filename.lower().endswith('.pdf'):
                errors.append(f"{file.filename}: Only PDF files are allowed")
                continue
            
            # Check file size (limit to 10MB)
            contents = await file.read()
            if len(contents) > 10 * 1024 * 1024:  # 10MB in bytes
                errors.append(f"{file.filename}: File too large. Maximum size is 10MB")
                continue
            
            # Generate unique filename
            file_id = str(uuid.uuid4())
            file_extension = ".pdf"
            unique_filename = f"{file_id}{file_extension}"
            file_path = UPLOAD_DIR / unique_filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                buffer.write(contents)
            
            uploaded_files.append({
                "file_id": file_id,
                "filename": file.filename,
                "saved_as": unique_filename,
                "file_size": len(contents),
                "file_path": str(file_path)
            })
            
        except Exception as e:
            errors.append(f"{file.filename}: Error saving file - {str(e)}")
    
    return JSONResponse(
        status_code=200,
        content={
            "message": f"Processed {len(files)} files",
            "uploaded_files": uploaded_files,
            "uploaded_count": len(uploaded_files),
            "errors": errors,
            "error_count": len(errors)
        }
    )

@app.get("/uploaded-files")
async def list_uploaded_files():
    try:
        files = []
        for file_path in UPLOAD_DIR.glob("*.pdf"):
            file_stats = file_path.stat()
            files.append({
                "filename": file_path.name,
                "file_size": file_stats.st_size,
                "upload_time": file_stats.st_mtime,
                "file_path": str(file_path)
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
