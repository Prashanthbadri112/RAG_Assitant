import gradio as gr
from uploads import upload_pdfs
from chat import ask_question, clear_chat

# Create Gradio Interface
with gr.Blocks(title="RAG Document Q&A System", theme=gr.themes.Soft()) as demo: # type: ignore
    
    gr.Markdown(
        """
        # 📚 RAG Document Q&A System
        Upload your PDF documents and ask questions based on their content!
        """
    )
    
    with gr.Tabs():
        # Tab 1: Upload Documents
        with gr.Tab("📤 Upload Documents"):
            gr.Markdown("### Upload PDF Documents")
            gr.Markdown("Upload one or more PDF files to add them to the knowledge base.")
            
            upload_files = gr.File(
                label="Select PDF Files",
                file_count="multiple",
                file_types=[".pdf"],
                type="filepath"
            )
            
            upload_button = gr.Button("Upload PDFs", variant="primary", size="lg")
            upload_output = gr.Textbox(label="Upload Status", lines=3)
            
            upload_button.click(
                fn=upload_pdfs,
                inputs=[upload_files],
                outputs=[upload_output]
            )
            
            gr.Markdown(
                """
                ### 💡 Tips:
                - Upload all your documents before asking questions
                - Supported format: PDF only
                - Documents will be processed and added to the vector database
                """
            )
        
        # Tab 2: Ask Questions
        with gr.Tab("💬 Ask Questions"):
            gr.Markdown("### Ask Questions About Your Documents")
            
            chatbot = gr.Chatbot(
                label="Conversation",
                height=500,
                type="messages",
            )
            
            with gr.Row():
                question_input = gr.Textbox(
                    label="Your Question",
                    placeholder="Type your question here... (e.g., What is diabetes?)",
                    lines=2,
                    scale=4
                )
                submit_button = gr.Button("Submit", variant="primary", scale=1)
            
            with gr.Row():
                clear_button = gr.Button("Clear Chat", variant="secondary")
            
            # Event handlers
            submit_button.click(
                fn=ask_question,
                inputs=[question_input, chatbot],
                outputs=[chatbot, question_input]
            )
            
            question_input.submit(
                fn=ask_question,
                inputs=[question_input, chatbot],
                outputs=[chatbot, question_input]
            )
            
            clear_button.click(
                fn=clear_chat,
                outputs=[chatbot, question_input]
            )
            
            gr.Markdown(
                """
                ### 📖 How to use:
                1. Make sure you've uploaded your documents in the "Upload Documents" tab
                2. Type your question in the text box above
                3. Press Enter or click Submit
                4. The system will answer based on the uploaded documents
                5. Sources will be shown at the bottom of each answer
                
                ### ⚠️ Note:
                - Answers are strictly based on uploaded documents only
                - If information is not found, the system will tell you
                """
            )
    
    gr.Markdown(
        """
        ---
        **Powered by:** FastAPI + LangChain + Groq + Pinecone + Google Gemini Embeddings
        """
    )

# Launch the app
if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False
    )