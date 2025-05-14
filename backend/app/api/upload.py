
from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from fastapi.responses import FileResponse
import aiofiles
import subprocess
router = APIRouter()


FILE_UPLOAD_DIR = "/home/abishekthamma/PycharmProjects/self_hosted/data/storage/prtts/uploads"
HTML_RESULTS_DIR = "/home/abishekthamma/PycharmProjects/self_hosted/data/storage/prtts/html_store"


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # file.filename: the original name e.g. "mydoc.pdf"
    # file.content_type: should be "application/pdf"
    print(f"Received file: {file.filename}, content type: {file.content_type}")

    if file.content_type != "application/pdf":
        print("Invalid file type")
        raise HTTPException(status_code=400, detail="Only PDFs allowed")


    # Save the file to the storage directory
    save_path = f"{FILE_UPLOAD_DIR}/{file.filename}"

    if os.path.exists(save_path):
        print(f"File {file.filename} already exists.")
        raise HTTPException(status_code=400, detail="File already exists")
    
    async with aiofiles.open(save_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    print(f"File saved to {save_path}")
    return {"filename": file.filename, "content_type": file.content_type}
    
    

@router.get("/files")
async def list_files():
    print("Listing files in storage directory")
    try:
        files = os.listdir(FILE_UPLOAD_DIR)
        processed_files = os.listdir(HTML_RESULTS_DIR)
        return [{"id": i, "name": file, "processed": file.split(".")[0] in processed_files} for i, file in enumerate(files)]
    except Exception as e:
        print(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@router.post("/files/{file_id}/extract")
async def extract_html(file_id: str):
    print(f"Extracting HTML for file ID: {file_id}")
    #raise HTTPException(status_code=400, detail="Invalid file ID")
    try:
        files = os.listdir(FILE_UPLOAD_DIR)
        if file_id not in files:
            raise HTTPException(status_code=404, detail="File not found")
        file_path = os.path.join(FILE_UPLOAD_DIR, file_id)
        output_folder = os.path.join(HTML_RESULTS_DIR, file_id.split(".")[0])
        os.makedirs(output_folder, exist_ok=True)
        command = [
            'pdftohtml',
            '-c',  # Preserve complex layout
            '-noframes',  # Avoid creating frames
            file_path,
            os.path.join(output_folder, 'index.html')  # Output file
        ]
        # Run the command and capture any errors
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Conversion output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e.stderr}")
        raise HTTPException(status_code=500, detail="Conversion failed")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"status": "ok", "message": "HTML extraction completed", "file_id": file_id}


@router.get("/files/{file_id}/audio")
async def get_audio(file_id: str):
    print(f"Getting audio for file ID: {file_id}")
    path  = "/home/abishekthamma/Downloads/carnatic/BMK-Nagumomu EP.mp3"

    if os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    #raise HTTPException(status_code=400, detail="Invalid file ID")
    
@router.get("/files/{file_id}/pages/{page_id}")
async def get_page(file_id: str, page_id: int):
    #raise HTTPException(status_code=400, detail="Invalid file ID")

    try:
        files = os.listdir(HTML_RESULTS_DIR)
        file_id = file_id.split(".")[0]
        print(f"Getting page {page_id} for file ID: {file_id}")
        print(f"Files in directory: {files}")
        if file_id not in files:
            raise HTTPException(status_code=404, detail="File not found")
        file_path = os.path.join(HTML_RESULTS_DIR, file_id, "index.html")
        print(f"File path: {file_path}")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Page not found")
        return FileResponse(file_path, media_type="text/html")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")