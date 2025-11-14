from logger import logger

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"running chain for input: {user_input}")

        # Invoke the chain with the question string
        result = chain.invoke(user_input)

        # The chain now returns a dict with 'response' and 'documents'
        response = {
            "response": result["response"],
            "sources": [
                {
                    "source": doc.metadata.get("source", "Unknown"),
                    "page": int(doc.metadata.get("page", 0)) + 1  # Pages are 0-indexed
                }
                for doc in result["documents"]
            ]
        }

        logger.debug(f"Chain response: {response}")
        return response

    except Exception as e:
        logger.exception("Error on query chain")
        raise e