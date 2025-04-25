import os
import shutil
from typing import List, Dict, Any
import time
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from django.conf import settings
from .embedding import get_embeddings
from .llm import CustomLLM


class RAGService:
    """Main RAG service implementation using LangChain with MMR retrieval"""

    def __init__(self, gpu_device=None):
        """
        Initialize RAG Service with MMR retrieval configuration

        :param gpu_device: Optional GPU device specification
        """
        self.persist_directory = os.path.join(settings.BASE_DIR, "chroma_db")
        self.collection_name = "pdf_collection"

        # Handle GPU device configuration if provided
        model_kwargs = {}
        if gpu_device is not None:
            model_kwargs["gpu_device"] = gpu_device

        # Initialize embeddings and LLM
        self.embeddings = get_embeddings()
        self.llm = (
            CustomLLM(**model_kwargs).get_llm()
            if model_kwargs
            else CustomLLM().get_llm()
        )

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
        ids = vectorstore.add_documents(chunks)
        return ids

    def query(self, query_text: str) -> Dict[str, Any]:
        """
        Process a query using Maximal Marginal Relevance (MMR) retrieval

        :param query_text: User's query string
        :return: Dictionary containing answer, sources, and timing information
        """
        start_time = time.time()

        # Get the vector store
        vectorstore = self.get_vectorstore()

        # Configure MMR retriever
        retriever = vectorstore.as_retriever(
            search_type="mmr",  # Maximal Marginal Relevance
            search_kwargs={
                "k": 10,  # Number of chunks to retrieve
                "fetch_k": 20,  # Number of documents to fetch before filtering
                "lambda_mult": 0.5,  # Balance between diversity and relevance
                # 0 = pure relevance, 1 = pure diversity
            },
        )

        # Create an enhanced prompt template
        template = """
        You are an AI assistant synthesizing comprehensive information from multiple documents.
        
        CONTEXT GUIDELINES:
        - Carefully analyze ALL provided context chunks
        - Synthesize information from different sources
        - Identify and highlight key insights across documents
        - If sources contain conflicting information, discuss the discrepancies
        
        CONTEXT:
        {context}
        
        QUESTION:
        {question}
        
        INSTRUCTIONS:
        1. Provide a thorough answer using information from ALL context chunks
        2. If no comprehensive answer is possible, explain what information is missing
        3. Cite sources for different pieces of information
        4. Demonstrate how information from multiple sources connects or provides a complete picture
        5. Be precise, informative, and transparent about the sources of your information
        
        ANSWER:
        """

        # Create prompt
        prompt = PromptTemplate.from_template(template)

        # Create the QA chain with MMR retrieval
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )

        # Run the chain
        result = qa_chain({"query": query_text})

        # Process sources with enhanced metadata
        sources = []
        unique_documents = set()
        for doc in result["source_documents"]:
            source = {
                "id": doc.metadata.get("chunk_id", "unknown"),
                "document_name": doc.metadata.get("name", "unknown"),
                "page": doc.metadata.get("page", 0),
                "source": doc.metadata.get("source", "unknown"),
                "content_preview": doc.page_content[:200] + "..."
                if len(doc.page_content) > 200
                else doc.page_content,
            }

            # Ensure unique documents are added
            if source["document_name"] not in unique_documents:
                sources.append(source)
                unique_documents.add(source["document_name"])

        # Calculate timing information
        end_time = time.time()
        total_time = int((end_time - start_time) * 1000)  # Convert to milliseconds

        # Return response
        return {
            "answer": result["result"],
            "sources": sources,
            "timing": {"total_ms": total_time},
        }
