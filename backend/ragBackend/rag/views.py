import os
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services.rag import RAGService
from .services.pdf import PDFProcessor
from .models import Document


@api_view(["POST"])
def query_endpoint(request):
    """Process a query through the RAG system"""
    try:
        query = request.data.get("query")
        if not query:
            return Response(
                {"error": "Query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Process the query
        rag_service = RAGService()
        result = rag_service.query(query)
        return Response(result)
    except Exception as e:
        import traceback

        return Response(
            {"error": str(e), "traceback": traceback.format_exc()},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def upload_document(request):
    """Upload and process a document"""
    try:
        if "file" not in request.FILES:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_file = request.FILES["file"]
        file_name = uploaded_file.name

        # Ensure the file is a PDF
        if not file_name.lower().endswith(".pdf"):
            return Response(
                {"error": "Only PDF files are supported"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save file to documents directory
        documents_dir = os.path.join(settings.MEDIA_ROOT, "documents")
        os.makedirs(documents_dir, exist_ok=True)

        file_path = os.path.join(documents_dir, file_name)

        with open(file_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Process the document
        processor = PDFProcessor()
        rag_service = RAGService()

        try:
            result = processor.process_pdf(file_path)
            chunks = result["chunks"]

            # Add to vector store
            rag_service.add_documents(chunks)

            # Save to database
            document = Document.objects.create(
                name=result["name"],
                file_path=file_path,
                file_type=result["file_type"],
                chunk_count=len(chunks),
                indexed=True,
            )

            return Response(
                {
                    "id": document.id,
                    "name": document.name,
                    "chunk_count": document.chunk_count,
                    "message": f"Successfully processed document with {len(chunks)} chunks.",
                }
            )
        except Exception as e:
            # Clean up the file if processing failed
            if os.path.exists(file_path):
                os.remove(file_path)
            raise e
    except Exception as e:
        import traceback

        return Response(
            {"error": str(e), "traceback": traceback.format_exc()},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def rebuild_index(request):
    """Rebuild the entire vector index from stored documents"""
    try:
        documents_dir = os.path.join(settings.MEDIA_ROOT, "documents")
        os.makedirs(documents_dir, exist_ok=True)

        processor = PDFProcessor()
        rag_service = RAGService()

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
                rag_service.add_documents(chunks)

                # Update or create document in database
                document, created = Document.objects.update_or_create(
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

        return Response(
            {
                "success": True,
                "documents_processed": len(processed_docs),
                "total_chunks": total_chunks,
                "message": f"Successfully processed {len(processed_docs)} documents with {total_chunks} chunks.",
            }
        )
    except Exception as e:
        import traceback

        return Response(
            {"error": str(e), "traceback": traceback.format_exc()},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
