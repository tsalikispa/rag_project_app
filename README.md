# PDF Question Answering System

A powerful MVC-based AI application that enables users to upload PDF documents and ask natural language questions about their content. The system leverages RAG (Retrieval-Augmented Generation) to provide accurate, contextually relevant answers based on document content.

![System Demo](docs/system_demo.gif)

## 🚀 Features

- **PDF Document Upload**: Easily upload and process PDF documents
- **Intelligent Question Answering**: Ask natural language questions about your documents
- **Source Attribution**: View the exact sources used to generate each answer
- **Vector Database**: ChromaDB for efficient document chunk retrieval
- **GPU-Accelerated Inference**: Optimized LLM performance using LlamaCpp

## 🏗️ Architecture

This application follows the Model-View-Controller (MVC) pattern with:

- **Frontend**: Angular 17 with Material UI
- **Backend**: Django with REST framework
- **Vector Database**: ChromaDB
- **NLP Framework**: LangChain
- **LLM**: DeepSeek-R1-Distill-Qwen-7B running on CUDA

![System Architecture](docs/architecture.png)

## 🔧 Technical Stack

### Backend (Django)
- Python 3.10+
- Django 4.2
- Django REST Framework
- LangChain
- ChromaDB
- PyPDF
- HuggingFace Transformers
- LlamaCpp

### Frontend (Angular)
- Angular 17
- Angular Material
- TypeScript
- RxJS
- NGX-TypeWriter (for animated text)

## 💻 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm/yarn
- CUDA-compatible GPU (recommended)

### Backend Setup
```bash
# Clone repository
git clone https://github.com/yourusername/pdf-qa-system.git
cd pdf-qa-system/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Start development server
ng serve
```

Visit `http://localhost:4200` to access the application.

## 📁 Project Structure

```
rag_project_app/
├── backend/                # Django backend
│   ├── rag/                # RAG application
│   │   ├── models.py       # Database models
│   │   ├── serializers.py  # API serializers
│   │   ├── views.py        # API endpoints
│   │   └── services/       # Business logic services
│   │       ├── rag.py      # RAG service implementation
│   │       ├── pdf.py      # PDF processing
│   │       ├── llm.py      # LLM integration
│   │       └── embedding.py # Embedding utilities
│   └── requirements.txt    # Python dependencies
├── frontend/               # Angular frontend
│   ├── src/                
│   │   ├── app/           
│   │   │   ├── rag-system/ # Main RAG component
│   │   │   └── welcome/    # Welcome component
│   │   └── services/       # Angular services
│   └── package.json        # Node dependencies
└── docs/                   # Documentation and images
    └── architecture.png    # Architecture diagram
```

## 📝 API Documentation

### Endpoints

- `POST /api/query/`: Submit a question about uploaded documents
- `POST /api/upload/`: Upload a PDF document
- `POST /api/rebuild-index/`: Rebuild the vector index

### Example API Usage

```python
# Query endpoint example
import requests
import json

response = requests.post(
    "http://localhost:8000/api/query/",
    headers={"Content-Type": "application/json"},
    data=json.dumps({"query": "What is the main topic of the document?"})
)

print(response.json())
```

## 📊 Performance

The system utilizes:
- Chunk size of 1000 characters with 200 character overlaps
- MMR retrieval with lambda_mult of 0.5 and k=10
- GPU acceleration with n_gpu_layers=32 (RTX 4070)
- all-MiniLM-L6-v2 embeddings (384 dimensions)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- HuggingFace for embedding models
- LangChain for the RAG framework
- Angular team for the frontend framework
