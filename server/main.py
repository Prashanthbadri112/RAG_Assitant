from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='myRag',description='API for myRag')

#cors setup
app.add_middleware(
    CORSMiddleware,
   allow_origins = ["*"],
   allow_methods =  ["*"],
   allow_headers =  ["*"]
)

@app.get('/')
def basic_setup():
    return {"message": "basic setup"}


