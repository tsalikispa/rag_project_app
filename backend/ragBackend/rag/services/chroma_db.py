# rag/services/chroma_db.py
import os
import shutil
from typing import List, Dict, Any
from langchain_chroma import Chroma
from langchain.schema import Document

from django.conf import settings
from .embedding import get_embeddings
from ..models import Document as DocumentModel


class ChromaDBService:
    """Service for interacting with the ChromaDB vector database"""

    def __init__(self):
        self.persist_directory = os.path.join(settings.BASE_DIR, "chroma_db")
        self.collection_name = "pdf_collection"
        self.embeddings = get_embeddings()

    def get_vectorstore(self):
        """Get or create the vector store"""
        try:
            return Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name,
            )
        except Exception as e:
            print(f"Error creating ChromaDB: {str(e)}")
            # If there's an error, try to recreate the database
            if os.path.exists(self.persist_directory):
                print(f"Recreating ChromaDB directory")
                shutil.rmtree(self.persist_directory, ignore_errors=True)

            # Try again with a fresh database
            return Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name,
            )

    def add_documents(self, chunks: List[Document]) -> List[str]:
        """Add document chunks to the vector store"""
        vectorstore = self.get_vectorstore()

        # Add documents and get the IDs
        return vectorstore.add_documents(chunks)

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Search for similar documents"""
        db = self.get_vectorstore()
        return db.similarity_search(query, k=k)

    def rebuild_index(self) -> Dict[str, Any]:
        """Rebuild the entire vector index from stored documents"""
        from .pdf import PDFProcessor

        # Create document processor
        processor = PDFProcessor()

        # Get all documents directory
        documents_dir = os.path.join(settings.MEDIA_ROOT, "documents")
        os.makedirs(documents_dir, exist_ok=True)

        # Get all PDF files in the documents directory
        pdf_files = [f for f in os.listdir(documents_dir) if f.lower().endswith(".pdf")]

        processed_docs = []
        total_chunks = 0

        for pdf_file in pdf_files:
            file_path = os.path.join(documents_dir, pdf_file)
            try:
                result = processor.process_pdf(file_path)
                chunks = result["chunks"]

                # Add to vector store
                self.add_documents(chunks)

                # Update or create document in database
                document, created = DocumentModel.objects.update_or_create(
                    file_path=file_path,
                    defaults={
                        "name": result["name"],
                        "file_type": result["file_type"],
                        "chunk_count": len(chunks),
                        "indexed": True,
                    },
                )

                processed_docs.append(document)
                total_chunks += len(chunks)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        return {
            "success": True,
            "documents_processed": len(processed_docs),
            "total_chunks": total_chunks,
            "message": f"Successfully processed {len(processed_docs)} documents with {total_chunks} chunks.",
        }
