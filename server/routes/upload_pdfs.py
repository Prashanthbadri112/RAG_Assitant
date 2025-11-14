from fastapi import APIRouter,UploadFile, File
from typing import List
from modules.load_vectorstore import load_vectorstore
from fastapi.responses import JSONResponse
from logger import logger


router = APIRouter()

@router.post('/upload_pdfs/')
async def upload_pdfs(files:List[UploadFile]=File(...)):
    try:
        logger.info(f"Number of files received: {len(files)}")
        for f in files:
            logger.info(f"Received file: {f.filename}")
        load_vectorstore(files)
        logger.info("Document added to vector store")
        return {
            "message":"Files processed and vectorstore updated"
        }
    except Exception as e:
        logger.exception("Error during pdf upload")
        return JSONResponse(status_code=500,content={"error":str(e)})
