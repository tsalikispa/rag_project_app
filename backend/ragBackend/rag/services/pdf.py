import os
from pathlib import Path
from typing import List, Dict, Any

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


class PDFProcessor:
    """Process PDF documents for indexing"""

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def process_pdf(self, file_path: str, document_name: str = None) -> dict:
        """Process a PDF into chunks with metadata"""
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        # Load the PDF
        loader = PyPDFLoader(file_path)
        raw_docs = loader.load()

        # Set document name if not provided
        if not document_name:
            document_name = Path(file_path).name

        # Split into chunks
        chunks = self.text_splitter.split_documents(raw_docs)

        # Add metadata to each chunk
        for i, chunk in enumerate(chunks):
            if not chunk.metadata.get("source"):
                chunk.metadata["source"] = file_path
            chunk.metadata["name"] = document_name
            chunk.metadata["chunk_id"] = i

        return {
            "name": document_name,
            "file_path": file_path,
            "file_type": "pdf",
            "chunks": chunks,
        }
