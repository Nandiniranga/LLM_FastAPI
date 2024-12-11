from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
import uvicorn
from secrets import token_hex
import time
from extractors import extract_content_from_pdf, extract_content_from_txt
from llm_integration import query_llm

# timestr = time.strftime("%Y%m%d-%H%M%S")
# app = FastAPI(title="Upload file using FastAPI")
    
# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_ext = file.filename.split(".").pop()
#     file_name = token_hex(10)
#     file_path = f"{file_name}.{file_ext}"
#     with open(file_path, "wb") as f:
#         content = await file.read()
#         f.write(content)
#     return {"success" : True , "file_path" : file_path , "message": "File uploaded successfully"}
#     with open(file_path, "wb") as f:
#          f.write(await file.read())

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    return {"filename": file.filename, "message": "File uploaded successfully"}
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", reload=True)

@app.post("/extract/")
async def extract_content(filename: str):
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    if file_path.suffix == ".pdf":
        content = extract_content_from_pdf(file_path)
    elif file_path.suffix == ".txt":
        content = extract_content_from_txt(file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    return content

@app.post("/query/")
async def query_content(filename: str, user_query: str):
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Extract content
    if file_path.suffix == ".pdf":
        content = extract_content_from_pdf(file_path)
    elif file_path.suffix == ".txt":
        content = extract_content_from_txt(file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Query the LLM
    llm_response = query_llm(content, user_query)
    return {"query": user_query, "response": llm_response}