from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handler import query_chain
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
import os

router = APIRouter()

@router.post('/ask_query')
async def user_query(question: str = Form(...)):
    try:
        logger.info(f"User Query : {question}")
        
        # Embed + Pinecone
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])  # type: ignore
        index = pc.Index(os.environ["PINECONE_INDEX_NAME"])  # type: ignore
        embedded_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        
        # Embed the query
        embedded_query = embedded_model.embed_query(question)
        logger.debug(f"Embedded query vector length: {len(embedded_query)}")
        
        # Query Pinecone
        res = index.query(vector=embedded_query, top_k=3, include_metadata=True)
        
        # DEBUG: Log the Pinecone response
        # logger.debug(f"Pinecone response: {res}")
        # logger.debug(f"Number of matches: {len(res.get('matches', []))}") # type: ignore
        
        # Create documents from matches
        docs = [
            Document(
                page_content=match['metadata'].get("text", ""),
                metadata=match['metadata']
            ) for match in res.get("matches", []) # type: ignore
        ]
        
        # DEBUG: Log the documents
        # logger.debug(f"Number of documents created: {len(docs)}")
        # for i, doc in enumerate(docs):
        #     logger.debug(f"Doc {i}: {doc.page_content[:100]}...")  # First 100 chars
        #     logger.debug(f"Doc {i} metadata: {doc.metadata}")
        
        # Check if documents are empty
        if not docs or all(not doc.page_content.strip() for doc in docs):
            logger.warning("No relevant documents found or all documents are empty!")
            return JSONResponse(
                status_code=200,
                content={
                    "response": "No relevant information found in the database for your query.",
                    "sources": []
                }
            )
        
        class SimpleRetriever(BaseRetriever):
            tags: Optional[List[str]] = Field(default_factory=list)
            metadata: Optional[dict] = Field(default_factory=dict)
            
            def __init__(self, documents: List[Document]):
                super().__init__()
                self._docs = documents
            
            def _get_relevant_documents(self, query: str) -> List[Document]:
                logger.debug(f"Retriever returning {len(self._docs)} documents")
                return self._docs
        
        retriever = SimpleRetriever(docs)
        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)
        
        logger.info("query Successfull")
        return result
        
    except Exception as e:
        logger.error(f"Error during processing of user query: {str(e)}")
        logger.exception("Full traceback:")
        return JSONResponse(status_code=500, content={"message": str(e)})
