import requests
import json
from config import API_URL
from typing import List, Tuple
from config import API_URL

def ask_question(question: str, chat_history: List[dict]):
    try:
        if not question.strip():
            return chat_history, ""

        response = requests.post(
            f"{API_URL}/ask_query",
            data={"question": question}
        )

        if response.status_code == 200:
            result = response.json()
            answer = result.get("response", "No response received")
            sources = result.get("sources", [])
            
            # Build source text
            sources_text = ""
            if sources:
                sources_text = "\n\n📚 **Sources:**\n"
                for idx, src in enumerate(sources, 1):
                    file = src.get("source", "Unknown").split("/")[-1]
                    page = src.get("page", "N/A")
                    sources_text += f"{idx}. {file} (Page {page})\n"

            full_answer = answer + sources_text

            # Append messages (new format)
            chat_history.append({"role": "user", "content": question, "avatar": "👤"})
            chat_history.append({"role": "assistant", "content": full_answer, "avatar": "🤖"})


            return chat_history, ""
        
        else:
            error_msg = f"❌ Error: {response.json().get('message', 'Unknown error')}"
            chat_history.append({"role": "user", "content": question})
            chat_history.append({"role": "assistant", "content": error_msg})
            return chat_history, ""

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": error_msg})
        return chat_history, ""


def clear_chat():
    """Clear the chat history"""
    return [], ""
