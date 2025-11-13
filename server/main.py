from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from exception_handler import expection_handling_middleware

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


