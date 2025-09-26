from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from typing import List, Dict
import uuid
import pandas as pd

from processing.loader import load_document_text
from processing.chunker import chunk_text
from processing.embedder import embed_chunks

app = FastAPI()

# Create uploads directory if it doesn't exist
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
    # 1. Validate file type
    if file.content_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}. Supported types are: {list(SUPPORTED_FILE_TYPES.keys())}")

    # 2. Save file temporarily
    file_extension = SUPPORTED_FILE_TYPES[file.content_type]
    file_id = str(uuid.uuid4())
    unique_filename = f"{file_id}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        contents = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        # 3. Load and process the document using your modules
        document_text = load_document_text(file_path, file.filename)
        if not document_text or not document_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the document.")

        # 4. Chunk the text
        chunks = chunk_text(document_text)

        # 5. Embed the chunks
        embeddings = embed_chunks(chunks)


        # In the future, you will add embedding and vector DB storage steps here.

        return JSONResponse(
            status_code=200,
            content={
                "message": "Document processed successfully.",
                "file_id": file_id,
                "filename": file.filename,
                "chunk_count": len(chunks),
                "embedding_count": len(embeddings),
                #"chunks": chunks, # For now, we return the chunks. Later, you might just return a success message.
            }
        )

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    finally:
        # 5. Clean up the saved file
        if file_path.exists():
            file_path.unlink()

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

@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    # Check if file is provided
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    allowed_extensions = ['.xlsx', '.xls', '.xlsm']
    if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls, .xlsm) are allowed")
    
    # Check file size (limit to 25MB for Excel files)
    contents = await file.read()
    if len(contents) > 25 * 1024 * 1024:  # 25MB in bytes
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 25MB")
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    unique_filename = f"{file_id}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
        
        # Try to read the Excel file to validate it and get basic info
        try:
            # Read Excel file to get sheet names and basic info
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            
            # Get info about each sheet
            sheets_info = []
            for sheet_name in sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                sheets_info.append({
                    "sheet_name": sheet_name,
                    "rows": len(df),
                    "columns": len(df.columns),
                    "column_names": df.columns.tolist()
                })
            
            excel_file.close()
            
        except Exception as excel_error:
            # If we can't read the Excel file, still save it but note the error
            sheets_info = []
            sheet_names = []
            excel_read_error = str(excel_error)
        
        response_data = {
            "message": "Excel file uploaded successfully",
            "file_id": file_id,
            "filename": file.filename,
            "saved_as": unique_filename,
            "file_size": len(contents),
            "file_path": str(file_path),
            "sheet_names": sheet_names,
            "sheets_info": sheets_info
        }
        
        # Add error info if Excel reading failed
        if 'excel_read_error' in locals():
            response_data["excel_read_error"] = excel_read_error
        
        return JSONResponse(
            status_code=200,
            content=response_data
        )
    
    except Exception as e:
        # Clean up file if something went wrong
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

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

@app.get("/excel/{file_id}")
async def get_excel_data(file_id: str, sheet_name: str = None, limit: int = 100):
    """
    Get data from an uploaded Excel file.
    
    Args:
        file_id: The unique ID of the uploaded file
        sheet_name: Optional sheet name to read from (if not provided, reads first sheet)
        limit: Maximum number of rows to return (default 100)
    """
    try:
        # Find the Excel file with the given ID
        excel_file_path = None
        for pattern in ["*.xlsx", "*.xls", "*.xlsm"]:
            for file_path in UPLOAD_DIR.glob(pattern):
                if file_path.stem.startswith(file_id):
                    excel_file_path = file_path
                    break
            if excel_file_path:
                break
        
        if not excel_file_path:
            raise HTTPException(status_code=404, detail="Excel file not found")
        
        # Read Excel file
        excel_file = pd.ExcelFile(excel_file_path)
        
        # If sheet_name is not provided, use the first sheet
        if sheet_name is None:
            sheet_name = excel_file.sheet_names[0]
        elif sheet_name not in excel_file.sheet_names:
            raise HTTPException(status_code=400, detail=f"Sheet '{sheet_name}' not found. Available sheets: {excel_file.sheet_names}")
        
        # Read the specified sheet
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        
        # Apply limit
        if limit > 0:
            df_limited = df.head(limit)
        else:
            df_limited = df
        
        # Convert to dict for JSON response
        data = df_limited.to_dict(orient='records')
        
        excel_file.close()
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Excel data retrieved successfully",
                "file_id": file_id,
                "sheet_name": sheet_name,
                "available_sheets": excel_file.sheet_names,
                "total_rows": len(df),
                "returned_rows": len(data),
                "columns": df.columns.tolist(),
                "data": data
            }
        )
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Excel file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading Excel file: {str(e)}")
