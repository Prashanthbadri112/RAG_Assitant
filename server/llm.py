from langchain_core.prompts import PromptTemplate
from langchain_community.chains import BaseRetrievalQA
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GRQO_API_KEY")

def get_llm_chain(retriver):
    llm = ChatGroq(
        model='llama3-70b-8192',
        api_key=GROQ_API_KEY # type: ignore
     )
    
    prompt = PromptTemplate(
        input_variables=["context","question"],
        template="""

        **context**
        {context}

        **question**
        {question}

        """
    )

    return BaseRetrievalQA.from_chain_type(
        llm = llm,
        retriver = retriver,
        chain_type = "stuff",
        chain_type_kwargs = {"prompt": prompt}
    )


