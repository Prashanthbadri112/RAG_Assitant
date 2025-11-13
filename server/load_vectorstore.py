import os, time
from dotenv import load_dotenv
from pathlib import Path
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community .document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_ENV="us-east-1"
PINECONE_INDEX_NAME="myRagindex"

os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY # type: ignore

UPLOAD_DIR = "./uploaded_documents"
os.makedirs(UPLOAD_DIR,exist_ok=True)

# Initialize pinecone instance
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud='aws',region=PINECONE_ENV)

existing_indexed = [index['name'] for index in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexed:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,
        spec=spec,
        metric='dotproduct'
    )

    while not pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)

# Load, Split, Embed and Upsert pdf docs content

def load_vectorstore(uploaded_files):
    embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    file_paths = []

    # Upload
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR)/file.filename
        with open(save_path,'wb') as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    # Split

    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        document = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunksize=500,chunk_overlap=100)
        chunks = splitter.split_documents(document)
        texts = [chunk.page_content for chunk in chunks]
        metadata = [chunk.metadata for chunk in chunks]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))] 

        # Embeddings
        print("Embedding the chunks")
        embedding = embed_model.embed_documents(texts)

        # Upsert
        print("Upserting embedding")
        with tqdm(total=len(embedding),desc="Upserting to pinecone") as progress:
            index.upsert(vectors=zip(ids,embedding,metadata)) # type: ignore
            progress.update(len(embedding))
        print(f"upload completed for {file_path}")

        





