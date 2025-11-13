from logger import logger
from fastapi.requests import Request
from fastapi.responses import JSONResponse

async def expection_handling_middleware(request:Request,call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception("UNHANDLED EXPECTION")
        return JSONResponse(status_code=500,content={"error":e})
 


