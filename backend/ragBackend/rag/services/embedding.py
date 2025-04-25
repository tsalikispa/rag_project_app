from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    """Create and configure the embeddings model"""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cuda"},
    )
