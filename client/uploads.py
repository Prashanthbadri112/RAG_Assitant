from typing import List, Tuple
import requests
from config import API_URL

def upload_pdfs(files: List[str]) -> str:
    """Upload PDF files to the backend"""
    try:
        if not files:
            return "❌ Please select at least one PDF file to upload."
        
        # Prepare files for upload
        files_to_upload = []
        for file_path in files:
            files_to_upload.append(
                ('files', (file_path.split('/')[-1], open(file_path, 'rb'), 'application/pdf'))
            )
        
        # Send request to backend
        response = requests.post(
            f"{API_URL}/upload_pdfs/",
            files=files_to_upload
        )
        
        # Close file handles
        for _, file_tuple in files_to_upload:
            file_tuple[1].close()
        
        if response.status_code == 200:
            return f"✅ Successfully uploaded {len(files)} PDF(s) and added to vector store!"
        else:
            return f"❌ Error: {response.json().get('error', 'Unknown error')}"
    
    except Exception as e:
        return f"❌ Error uploading files: {str(e)}"
