from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_groq import ChatGroq
from modules.prompts import med_prompt
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain(retriever):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY  # type: ignore
    )

    prompt = med_prompt
    
    # Helper function to format context from documents
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])
    
    # Create a chain that retrieves documents and generates response
    rag_chain_from_docs = (
        {
            "context": lambda x: format_docs(x["documents"]),
            "question": lambda x: x["question"]
        }
        | prompt 
        | llm 
        | StrOutputParser()
    )
    
    # Wrap to include source documents in output
    rag_chain = RunnableParallel(
        {
            "documents": retriever,
            "question": RunnablePassthrough()
        }
    ).assign(response=rag_chain_from_docs)
    
    return rag_chain