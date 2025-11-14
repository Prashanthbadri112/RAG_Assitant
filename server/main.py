from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from exception_handler import expection_handling_middleware
from routes.upload_pdfs import router as upload_router
from routes.user_query import router as ask_router

app = FastAPI(title='myRag',description='API for myRag')

#cors setup
app.add_middleware(
    CORSMiddleware,
   allow_origins = ["*"],
   allow_methods =  ["*"],
   allow_headers =  ["*"],
   allow_credentials = ["*"] # type: ignore
)

app.middleware("http")(expection_handling_middleware)


# routers

# 1. upload pdfs documents
app.include_router(upload_router)
# 2. asking query
app.include_router(ask_router)